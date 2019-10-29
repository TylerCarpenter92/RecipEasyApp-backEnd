from django.http import HttpResponseServerError
from django.contrib.auth.models import User
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from recipEasyApp.models import *
from .ingredient import IngredientSerializer



class RecipeSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for recipe

    Arguments:
        serializers
    """
    # ingredient_list = IngredientSerializer(many=True)
    class Meta:
        model = Ingredient
        url = serializers.HyperlinkedIdentityField(
            view_name='ingredient',
            lookup_field='id'
        )
        fields = ('id', 'url', 'name', 'instructions', 'time_to_cook', 'link_to_page', 'line_items')
        depth = 1


class Recipes(ViewSet):

    def create(self, request):
        """Handle POST operations


        Returns:
            Response -- JSON serialized recipe instance
        """

        new_recipe = Recipe()
        new_recipe.name = request.data["name"]
        customer = Customer.objects.get(user=request.auth.user)
        new_recipe.customer = customer

        new_recipe.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order

        Author: Curt Cato
        Purpose: Allow a user to communicate with the Bangazon database to retrieve one order
        Method:  GET

        Returns:
            Response -- JSON serialized order instance
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)

    def update(self, request, pk=None):
        """Handle PUT requests for a recipe

        Purpose: Allow a user to update an order via the Bangazon DB
        Method: PUT

        Returns:
            Response -- Empty body with 204 status code
        """
        recipe = Recipe.objects.get(pk=pk)
        recipe.name = request.data["name"]
        recipe.instructions = request.data["instructions"]
        recipe.time_to_cook = request.data['time_to_cook']
        recipe.link_to_page = request.data['link_to_page']
        recipe.save()

        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk=None):
        """Handle DELETE requests for a recipe are

        Purpose: Allow a user to delete an order from the DB
        Method: DELETE

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            recipe = Recipe.objects.get(pk=pk)
            recipeingredient = RecipeIngredient.objects.all()
            recipeingredient = recipeingredient.filter(recipe=recipe)
            for item in recipeingredient:
                item.delete()
            recipe.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except Recipe.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to orders resource


        Returns:
            Response -- JSON serialized list of orders
        """
        recipes = Recipe.objects.all()
        customer = Customer.objects.get(user=request.auth.user)

        recipes = recipes.filter(customer=customer)

        serializer = RecipeSerializer(
            recipes, many=True, context={'request': request}
            )
        return Response(serializer.data)