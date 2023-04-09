from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, verbose_name='ФИО')
    email = models.EmailField(unique=True, verbose_name='Почта')
    phone_number = models.CharField(max_length=20, verbose_name='Номер телефона')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name or self.email
