# analytics/serializers.py

from rest_framework import serializers
from .models import Customers, Product, Order,SalesData,SalesGrowth,Address,Repeat

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'state', 'postal_code', 'country']

class CustomerSerializer(serializers.ModelSerializer):
    default_address = AddressSerializer()

    class Meta:
        model = Customers
        fields = ['id', 'first_name', 'last_name', 'email', 'phone_number', 'default_address', 'created_at', 'updated_at']

    def create(self, validated_data):
        address_data = validated_data.pop('default_address', None)
        address_instance = None
        if address_data:
            address_instance = Address.objects.create(**address_data)
        customer = Customers.objects.create(default_address=address_instance, **validated_data)
        return customer
    
    def update(self, instance, validated_data):
        address_data = validated_data.pop('default_address', None)
        if address_data:
            address_instance, created = Address.objects.update_or_create(
                id=instance.default_address.id, defaults=address_data
            )
            instance.default_address = address_instance
        instance.customer_id = validated_data.get('customer_id', instance.customer_id)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.save()
        return instance
    
class RepeatCustomerSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Repeat
        fields = ['customer', 'first_name', 'amount',]

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
        
        
class SalesDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesData
        fields = '__all__'

class SalesGrowthSerializer(serializers.ModelSerializer):
    class Meta:
        model = SalesGrowth
        fields = '__all__'