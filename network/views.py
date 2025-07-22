from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from network.models import NetworkPoint, Contact, Product
from network.serializers import (
    NetworkPointSerializer,
    ContactSerializer,
    ProductSerializer,
)


class NetworkPointViewSet(viewsets.ModelViewSet):
    queryset = NetworkPoint.objects.all()
    serializer_class = NetworkPointSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["contacts__country"]
    search_fields = ["contacts__country", "contacts__city", "name", "level"]
    ordering_fields = ["name", "level", "created_at"]
    ordering = ["name"]


class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
