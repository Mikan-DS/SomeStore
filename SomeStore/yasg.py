from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="GoodStore",
      default_version='v1',
      description="Этот проект представляет собой интернет-магазин, в котором пользователи могут просматривать "
                  "товары, добавлять их в корзину и оформлять заказы. Администраторы могут просматривать заказы, "
                  "управлять товарами и управлять пользователями. Проект реализован на Django и использует PostgreSQL "
                  "в качестве базы данных. В проекте применяются системы аутентификации и авторизации пользователей, "
                  "а также возможность для администраторов модерировать заказы и товары.",
      contact=openapi.Contact(email="MikanDrawChannel@gmail.com", name="Salem"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path(r'swagger(?P<format>\\.json|\\.yaml)', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path(r'swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(r'redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
