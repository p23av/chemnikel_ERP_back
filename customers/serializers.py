from rest_framework import serializers
from .models import Customer, ContactPerson, Product

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = ['id', 'name', 'tax_id', 'email', 'phone', 'is_active']

# Сериализатор для ContactPerson
class ContactPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPerson
        fields = '__all__'

# Сериализатор для Product
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'