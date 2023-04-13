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

    path('my_orders/', views.under_construction, name='my_orders'),

    path('orders/', views.under_construction, name='orders'),
    path('moderate_orders/', views.under_construction, name='moderate_orders'),
    path('archive_orders/', views.under_construction, name='archive_orders'),

]
