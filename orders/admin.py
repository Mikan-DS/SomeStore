from django import forms
from django.contrib import admin
from django.shortcuts import redirect, render

from .models import Order, ReviewedOrder, Product

class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline,]
    list_display = ['id', 'user', 'saved_date', 'get_status']
    ordering = ['-id']
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'

    def get_status(self, obj):
        reviewed_order = ReviewedOrder.objects.filter(order=obj).first()
        if reviewed_order is None:
            return 'На рассмотрении'
        else:
            return reviewed_order.get_status()
    get_status.short_description = 'Статус'
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price']
    ordering = ['-id']
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'

# @admin.register(ReviewedOrder)
# class ReviewedOrderAdmin(admin.ModelAdmin):
#     list_display = ['id', 'order', 'admin_user', 'decision_date', 'rejection_reason', 'get_status']
#     ordering = ['-id']
#     verbose_name = 'Рассмотренный заказ'
#     verbose_name_plural = 'Рассмотренные заказы'
#     actions = ['approve_orders', 'reject_orders']
#
#     def approve_orders(self, request, queryset):
#         queryset.update(rejection_reason=None)
#     approve_orders.short_description = 'Принять выбранные заказы'
#
#     def reject_orders(self, request, queryset):
#         rejection_reason = request.POST.get('rejection_reason')
#         if not rejection_reason:
#             self.message_user(request, 'Вы должны указать причину отказа')
#             return
#         queryset.update(rejection_reason=rejection_reason)
#     reject_orders.short_description = 'Отклонить выбранные заказы'
#
#     def get_status(self, obj):
#         return obj.get_status()
#     get_status.short_description = 'Статус'


class RejectOrdersForm(forms.ModelForm):
    rejection_reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ReviewedOrder
        fields = ['rejection_reason']

@admin.register(ReviewedOrder)
class ReviewedOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'admin_user', 'decision_date', 'rejection_reason', 'get_status']
    ordering = ['-id']
    verbose_name = 'Рассмотренный заказ'
    verbose_name_plural = 'Рассмотренные заказы'
    actions = ['approve_orders', 'reject_orders']

    def approve_orders(self, request, queryset):
        queryset.update(rejection_reason=None)
    approve_orders.short_description = 'Принять выбранные заказы'

    def reject_orders(self, request, queryset):
        form = None
        if 'apply' in request.POST:
            form = RejectOrdersForm(request.POST)
            if form.is_valid():
                rejection_reason = form.cleaned_data['rejection_reason']
                queryset.update(rejection_reason=rejection_reason)
                self.message_user(request, f'{queryset.count()} заказов было отклонено')
                return redirect(request.get_full_path())
        if not form:
            form = RejectOrdersForm()
        return render(request, 'admin/reject_orders.html', {'form': form, 'queryset': queryset})
    reject_orders.short_description = 'Отклонить выбранные заказы'

    def get_status(self, obj):
        return obj.get_status()
    get_status.short_description = 'Статус'

