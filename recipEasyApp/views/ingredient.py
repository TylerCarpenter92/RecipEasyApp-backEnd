from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from recipEasyApp.models import *
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class IngredientSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for ingredients

        Arguments:
        serializers.HyperlinkedModelSerializer
    """
    # This meta defines the field and the model that is being used
    class Meta:
        model = Ingredient
        url = serializers.HyperlinkedIdentityField(
        view_name='ingredient',
        lookup_field='id'
        )

        fields = ('id', 'name', 'location')
        depth = 1


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

        # city = self.request.query_params.get('city', None)
        # quantity = self.request.query_params.get('quantity', None)
        # order = self.request.query_params.get('order_by', None)
        # direction = self.request.query_params.get('direction', None)
        # product_type = self.request.query_params.get('product_type', None)

        # if order is not None:
        #     filter = order

        #     if direction is not None:
        #         if direction == "desc":
        #             filter = f'-{filter}'

        #     products = products.order_by(filter)

        # if city == "":
        #     products = Product.objects.all()
        # elif city is not None:
        #     products = Product.objects.filter(city=city)

        # if quantity is not None:
        #     product_list = list()
        #     quantity = int(quantity)
        #     length = len(products)
        #     count = 0
        #     for product in products:
        #         count += 1
        #         if count - 1 + quantity >= length:
        #             if product.quantity > 0:
        #                 product_list.append(product)
        #             if count == length:
        #                 products = product_list
        #                 break


        serializer = IngredientSerializer(
            ingredients, many=True, context={'request': request})
        return Response(serializer.data)