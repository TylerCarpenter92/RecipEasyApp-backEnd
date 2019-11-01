"""View module for handling requests about park areas"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from recipEasyApp.models import Location

class LocationSerializer(serializers.HyperlinkedModelSerializer):
    """JSON serializer for product types

    Arguments:
        serializers
    """

    class Meta:
        model = Location
        url = serializers.HyperlinkedIdentityField(
            view_name='location',
            lookup_field='id'
        )
        fields = ('id', 'url', 'location')


class Locations(ViewSet):
    """Product types for RecipEasy"""

    permission_classes = (IsAuthenticatedOrReadOnly,)

    def retrieve(self, request, pk=None):
        """Handle GET requests for single product type

        Returns:
            Response -- JSON serialized ProductType instance
        """
        try:
            location = Location.objects.get(pk=pk)
            serializer = LocationSerializer(Location, context={'request': request})
            return Response(serializer.data)
        except Exception as ex:
            return HttpResponseServerError(ex)


    def list(self, request):
        """Handle GET requests to product types resource

        Returns:
            Response -- JSON serialized list of product types
        """
        locations = Location.objects.all()

        serializer = LocationSerializer(
            locations, many=True, context={'request': request})
        return Response(serializer.data)