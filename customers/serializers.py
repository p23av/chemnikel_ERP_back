from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        # fields = '__all__'
        fields = ['id', 'name', 'tax_id', 'email', 'phone', 'is_active']