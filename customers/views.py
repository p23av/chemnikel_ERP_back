from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Customer, ContactPerson, Product
from .serializers import CustomerSerializer, ContactPersonSerializer, ProductSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      headers = self.get_success_headers(serializer.data)
      return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ContactPersonViewSet(viewsets.ModelViewSet):
    queryset = ContactPerson.objects.all()
    serializer_class = ContactPersonSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer