from django import forms
from django.contrib import admin, messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html

from .models import Order, ReviewedOrder, Product


class ProductInline(admin.TabularInline):
    model = Product
    extra = 1
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInline, ]
    list_display = ['id', 'user', 'saved_date', 'get_status', 'change_status_button']
    ordering = ['-id']
    verbose_name = 'Заказ'
    verbose_name_plural = 'Заказы'

    def get_status(self, obj):
        return obj.get_status()

    get_status.short_description = 'Статус'

    def change_status_button(self, obj):
        reviewed_order = ReviewedOrder.objects.filter(order=obj).first()

        if reviewed_order is None:

            url = reverse('admin:orders_reviewedorder_add') + f"?order={obj.id}"

        else:
            url = reverse('admin:orders_reviewedorder_change', args=[reviewed_order.id])

        return format_html('<a class="button" href="{}">Изменить статус</a>', url)

    change_status_button.short_description = ''
    change_status_button.allow_tags = True


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'id', 'price']
    ordering = ['-id']
    verbose_name = 'Товар'
    verbose_name_plural = 'Товары'


class RejectOrdersForm(forms.ModelForm):
    rejection_reason = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = ReviewedOrder
        fields = ['rejection_reason']


class ReviewedOrderForm(forms.ModelForm):
    class Meta:
        model = ReviewedOrder
        fields = ['order', 'decision_date', 'rejection_reason']  # 'admin_user',
        labels = {
            'order': "Заказ",
            'admin_user': 'Администратор',
            'decision_date': 'Дата решения',
            'decision': 'Решение',
            'rejection_reason': 'Причина отклонения',
            'approver': 'Администратор',

        }

    APPROVE = 'approve'
    REJECT = 'reject'

    decision = forms.ChoiceField(choices=((APPROVE, 'Принять'), (REJECT, 'Отклонить')), widget=forms.RadioSelect,
                                 label='Решение', initial=APPROVE)

    approver = forms.CharField(label="Администратор")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk is not None:
            self.fields['order'].widget = forms.HiddenInput()

        if self.instance.rejection_reason is None:
            self.fields['decision'].initial = self.APPROVE
        else:
            self.fields['decision'].initial = self.REJECT

        self.fields['rejection_reason'].initial = self.instance.rejection_reason

        self.fields['approver'].initial = self.instance.admin_user

        self.fields['decision_date'].widget.attrs['readonly'] = True  # тут по вкусу
        self.fields['approver'].widget.attrs['readonly'] = True

    def clean(self):
        cleaned_data = super().clean()
        decision = cleaned_data.get('decision')
        rejection_reason = cleaned_data.get('rejection_reason')

    def save(self, commit=True):
        reviewed_order = super().save(commit=False)
        decision = self.cleaned_data.get('decision')
        rejection_reason = self.cleaned_data.get('rejection_reason')

        reviewed_order.decision_date = timezone.now()
        reviewed_order.decision_date = timezone.now()

        if decision == 'approve':
            reviewed_order.rejection_reason = None
        else:
            reviewed_order.rejection_reason = rejection_reason

        if commit:
            reviewed_order.save()

        return reviewed_order


@admin.register(ReviewedOrder)
class ReviewedOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'admin_user', 'decision_date', 'rejection_reason', 'get_status']
    ordering = ['-id']
    verbose_name = 'Рассмотренный заказ'
    verbose_name_plural = 'Рассмотренные заказы'
    actions = ['approve_orders', 'reject_orders']

    fieldsets = (
        ('Информация', {
            'fields': ('order', 'approver', 'decision_date')
        }),
        ('Статус', {
            'classes': ('wide',),
            'fields': ('decision', 'rejection_reason')
        }),
    )

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

    def get_changeform_initial_data(self, request):

        initial = super().get_changeform_initial_data(request)

        initial["decision_date"] = timezone.now()
        initial["admin_user"] = request.user

        return initial

    def get_form(self, request, obj=None, **kwargs):
        form = ReviewedOrderForm
        form.request = request
        return form

    def save_form(self, request, form, change):

        form.instance.admin_user = request.user

        return form.save(commit=False)

    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj is not None and obj.decision_date is not None:
            self.message_user(request, 'Чтобы отправить заказ обратно на рассмотрение удалите запись',
                              level=messages.WARNING)
        return super().change_view(request, object_id, form_url, extra_context=extra_context)
