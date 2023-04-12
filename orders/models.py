from django.db import models
from users.models import CustomUser


class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name="Клиент")
    saved_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата сохранения')
    comment = models.TextField(blank=True, null=True, verbose_name='Комментарий')

    def __str__(self):
        return f"Заказ #{self.id}: {self.user} {self.saved_date}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def get_status(self):
        reviewed_order = ReviewedOrder.objects.filter(order=self).first()
        if reviewed_order is None:
            return 'На рассмотрении'
        else:
            return reviewed_order.get_status()


class Product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='products', verbose_name='В заказе')
    url = models.URLField(verbose_name='URL страницы')
    name = models.CharField(max_length=255, verbose_name='Название')
    photo = models.ImageField(upload_to='orders/', null=True, blank=True, verbose_name='Фото')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена')
    position_number = models.IntegerField(default=1, verbose_name='Номер позиции')
    quantity = models.IntegerField(default=1, verbose_name='Количество')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return f"{self.name} - {self.price}"


class ReviewedOrder(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='reviewed_order', verbose_name='Заказ')
    admin_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Администратор')
    decision_date = models.DateTimeField(verbose_name='Дата принятия решения')
    rejection_reason = models.TextField(null=True, blank=True, verbose_name='Причина отказа')

    def get_status(self):
        if self.rejection_reason is None:
            return 'Принято'
        else:
            return 'Отказано'

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'Рассмотренный заказ'
        verbose_name_plural = 'Рассмотренные заказы'
