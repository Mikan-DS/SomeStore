from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('login', views.under_construction, name='login'),
    path('orders', views.under_construction, name='orders'),
    path('moderate_orders', views.under_construction, name='moderate_orders'),
    path('cart', views.under_construction, name='cart'),
    path('archive_orders', views.under_construction, name='archive_orders'),

    path('<path:dummy>', views.under_construction, name='under_construction'),
]
