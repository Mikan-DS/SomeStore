from rest_framework import serializers

from orders.models import Product, ReviewedOrder, Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Order
        fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class ReviewedOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewedOrder
        fields = '__all__'
