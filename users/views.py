"""
 Я бы еще посидел с API SWAGGER

"""

from rest_framework.authtoken.models import Token

from orders.models import Product, Order, ReviewedOrder
from users.models import CustomUser
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework import permissions, status, authentication
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from orders.serializers import ProductSerializer, OrderSerializer, ReviewedOrderSerializer

@swagger_auto_schema(method='get', operation_summary='Get All Orders', responses={200: OrderSerializer(many=True)})
@api_view(['GET'])
def all_orders(request):
    """
    List all orders.
    """
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='post', operation_summary='Create Order', responses={201: openapi.Response('Order created successfully', OrderSerializer)})
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def create_order(request):
    """
    Create an order.
    """
    user = request.user
    try:
        order = Order.objects.create(user=user)
        order.save()
        return Response({'message': 'Order created successfully', 'order_id': order.id}, status=status.HTTP_201_CREATED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@swagger_auto_schema(method='get', operation_summary='Get My Orders', responses={200: OrderSerializer(many=True)})
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def my_orders(request):
    """
    List all orders belonging to the authenticated user.
    """
    user = request.user
    orders = Order.objects.filter(user=user)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='post', operation_summary='Add Product to Order', responses={200: openapi.Response('Product added to the order', ProductSerializer)}, request_body=ProductSerializer)
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def add_product(request):
    """
    Add a product to an order.
    """
    user = request.user
    order_id = request.data.get('order_id')
    product_id = request.data.get('product_id')
    quantity = request.data.get('quantity')
    order = get_object_or_404(Order, id=order_id, user=user)
    product = get_object_or_404(Product, id=product_id)
    order.add_product(product, quantity)
    return Response({'message': 'Product added to the order', 'product': ProductSerializer(product).data})

@swagger_auto_schema(method='delete', operation_summary='Remove Product from Order', responses={200: openapi.Response('Product removed from the order', ProductSerializer)})
@api_view(['DELETE'])
@permission_classes([permissions.IsAuthenticated])
def remove_product(request):
    """
    Remove a product from an order.
    """
    user = request.user
    order_id = request.data.get('order_id')
    product_id = request.data.get('product_id')
    order = get_object_or_404(Order, id=order_id, user=user)
    product = get_object_or_404(Product, id=product_id)
    order.remove_product(product)
    return Response({'message': 'Product removed from the order', 'product': ProductSerializer(product).data})

@swagger_auto_schema(method='post', operation_summary='Register', responses={201: openapi.Response('User created successfully')})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    """
    Register a new user.
    """
    full_name = request.data.get('full_name')
    email = request.data.get('email')
    phone_number = request.data.get('phone_number')
    password = request.data.get('password')
    user = CustomUser.objects.create_user(email=email, password=password, full_name=full_name, phone_number=phone_number)
    user.save()
    return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

@swagger_auto_schema(method='post', operation_summary='Login', responses={200: openapi.Response('Token'), 401: 'Invalid credentials'})
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    """
    Login a user.
    """
    email = request.data.get('email')
    password = request.data.get('password')
    user = authentication.authenticate(email=email, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@swagger_auto_schema(method='post', operation_summary='Moderate Order', responses={200: ReviewedOrderSerializer})
@api_view(['POST'])
@permission_classes([permissions.IsAdminUser])
def moderate_order(request, order_id:int):
    """
    Moderate an order.
    """
    order = get_object_or_404(Order, id=order_id)
    if order.reviewed_order is None:
        reviewed_order = ReviewedOrder(order=order)
        reviewed_order.save()
    else:
        reviewed_order = order.reviewed_order
    serializer = ReviewedOrderSerializer(reviewed_order)
    return Response(serializer.data)

