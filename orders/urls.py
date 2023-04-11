from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('cart/', views.under_construction, name='cart'),

    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),

    path('my_orders/', views.under_construction, name='my_orders'),

    path('orders/', views.under_construction, name='orders'),
    path('moderate_orders/', views.under_construction, name='moderate_orders'),
    path('archive_orders/', views.under_construction, name='archive_orders'),

    path('<path:dummy>', views.under_construction, name='under_construction'),
]
