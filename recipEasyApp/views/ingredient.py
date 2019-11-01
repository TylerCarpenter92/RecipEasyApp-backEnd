from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from recipEasyApp.models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .recipeingredient import RecipeIngredientSerializer


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for ingredients

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    recipe_ingredient = RecipeIngredientSerializer(many=True)
    class Meta:
        model = Ingredient
        url = serializers.HyperlinkedIdentityField(
        view_name='ingredient',
        lookup_field='id'
        )

        fields = ('id', 'name', 'location', 'recipe_ingredient')
        depth = 2


class Ingredients(ViewSet):
    """Handle POST operations
        Returns:
            Response -- JSON serialized ingredient instance
        """
    permission_classes = (IsAuthenticatedOrReadOnly,)
    def create(self, request):
        new_ingredient = Ingredient()
        new_ingredient.customer = Customer.objects.get(user=request.auth.user)
        new_ingredient.location = Location.objects.get(pk=request.data['location_id'])
        new_ingredient.name = request.data["name"]

        new_ingredient.save()
        serializer = IngredientSerializer(new_ingredient, context={'request': request})
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single ingredient
        Returns:
            Response -- JSON serialized park area instance
        """
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            serializer = IngredientSerializer(ingredient, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for an ingredient
        Returns:
            Response -- Empty body with 204 status code
        """
        ingredient = Ingredient.objects.get(pk=pk)
        product.name = request.data['name']
        ingredient.location = Location.objects.get(pk=request.data['location_id'])


        ingredient.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single ingredient are
        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            ingredient = Ingredient.objects.get(pk=pk)
            ingredient.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Ingredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to ingredients resource
        Returns:
            Response -- JSON serialized list of ingredients
        """
        ingredients = Ingredient.objects.all()  # This is my query to the database

        serializer = IngredientSerializer(
            ingredients, many=True, context={'request': request})
        return Response(serializer.data)