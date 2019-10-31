from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from recipEasyApp.models import RecipeIngredient, Recipe, Ingredient

# Author: Amber Gooch
# Purpose: Allow a user to communicate with the Bangazon database to GET POST and DELETE order/product entries.
# Methods: GET POST DELETE


class RecipeIngredientSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for order/product join table

    Arguments:
        serializers
    """
    class Meta:
        model = RecipeIngredient
        url = serializers.HyperlinkedIdentityField(
            view_name='recipeingredient',
            lookup_field='id'
        )
        fields = ('id', 'recipe', 'ingredient', 'amount', 'extra_instructions')
        depth = 2


class RecipeIngredients(ViewSet):

    def create(self, request):
        """Handle POST operations

        Returns:
            Response -- JSON serialized RecipeIngredient instance
        """
        ingredient = Ingredient.objects.get(name=request.data['name'])
        if not ingredient:
            ingredient = Ingredient()
            ingredient.name = request.data['name']
            ingredient.location = request.data['location']
            ingredient.save()

        new_recipeingredient = RecipeIngredient()

        new_recipeingredient.recipe = Recipe.objects.get(pk=request.data["recipe_id"])
        new_recipeingredient.ingredient = ingredient
        new_recipeingredient.amount = request.data['amount']
        new_recipeingredient.extra_instructions = request.data['extra_instructions']

        new_recipeingredient.save()

        serializer = RecipeIngredientSerializer(new_recipeingredient, context={'request': request})

        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single order/product relationship

        Returns:
            Response -- JSON serialized RecipeIngredient instance
        """
        try:
            recipeingredient = RecipeIngredient.objects.get(pk=pk)
            serializer = RecipeIngredientSerializer(recipeingredient, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    #   def update(self, request, pk=None):
    #     """Handle PUT requests for a recipe

    #     Purpose: Allow a user to update an order via the Bangazon DB
    #     Method: PUT

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """


    def destroy(self, request, pk=None):
        """Handle DELETE requests for a single order/product relationship

        Returns:
            Response -- 200, 404, or 500 status code
        """
        try:
            recipeingredient = RecipeIngredient.objects.get(pk=pk)
            recipeingredient.delete()

            return Response({}, status=status.HTTP_204_NO_CONTENT)

        except RecipeIngredient.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

        except Exception as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        recipeingredients = RecipeIngredient.objects.all()

        serializer = RecipeIngredientSerializer(
            recipeingredients, many=True, context={'request': request})
        return Response(serializer.data)