from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from recipEasyApp.models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class MealPlanningSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for ingredients

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    class Meta:
        model = MealPlanning
        url = serializers.HyperlinkedIdentityField(
        view_name='mealplanning',
        lookup_field='id'
        )

        fields = ('id', 'customer', 'recipe', 'date')
        depth = 2


class MealPlannings(ViewSet):
    """Handle POST operations
        Returns:
            Response -- JSON serialized ingredient instance
        """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):
        new_mealplanning = MealPlanning()
        new_mealplanning.customer = Customer.objects.get(user=request.auth.user)
        new_mealplanning.recipe = Recipe.objects.get(pk=request.data['recipe_id'])
        new_mealplanning.date = request.data['date']

        new_mealplanning.save()
        serializer = MealPlanningSerializer(new_mealplanning, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ingredient
        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            mealplanning = MealPlanning.objects.get(pk=pk)
            serializer = MealPlanningSerializer(mealplanning, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an ingredient
        Returns:
            Response -- Empty body with 204 status code
        """
        mealplanning = MealPlanning.objects.get(pk=pk)
        mealplanning.date = request.data['date']


        mealplanning.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single ingredient are
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            mealplanning = MealPlanning.objects.get(pk=pk)
            mealplanning.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except MealPlanning.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to ingredients resource
        Returns:
            Response -- JSON serialized list of ingredients
        """
        mealplanning = MealPlanning.objects.all()  # This is my query to the database

        serializer = MealPlanningSerializer(
            mealplanning, many=True, context={'request': request})
        return Response(serializer.data)