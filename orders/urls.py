from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('cart/', views.cart, name='cart'),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/place_order/', views.place_order, name='place_order'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),

    path('my_orders/', views.my_orders, name='my_orders'),

    path('orders/order/<int:order_id>', views.order_detail, name='order'),
    path('moderate_orders/order/<int:order_id>', views.moderate_order, name='order_moderate'),

    path('orders/', views.all_orders, name='orders'),
    path('moderate_orders/', views.moderate_orders, name='moderate_orders'),
    path('archive_orders/', views.archive_orders, name='archive_orders'),

]
