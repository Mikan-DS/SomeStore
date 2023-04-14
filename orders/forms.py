from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import EmailValidator, RegexValidator
from django.utils.translation import gettext_lazy as _

from orders.models import Product, ReviewedOrder

CustomUser = get_user_model()


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label=_('ФИО'))
    email = forms.EmailField(label=_('Электронная почта'), validators=[EmailValidator()])
    phone_regex = RegexValidator(
        regex=r'^\+?[78][-\\(]?\d{3}\)?-?\d{3}-?\d{2}-?\d{2}$',
        message=_("Номер телефона (РФ) должен быть в формате: '+7(999)999-9999'."))
    phone_number = forms.CharField(validators=[phone_regex], max_length=20, label=_('Номер телефона'))

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('full_name', 'email', 'phone_number')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Пользователь с таким адресом электронной почты уже существует.')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.save()
        return user


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('url', 'name', 'photo', 'price', 'position_number', 'quantity')
        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'position_number': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
        }


class ReviewedOrderForm(forms.ModelForm):
    status = forms.ChoiceField(
        label='Статус заказа',
        choices=(('review', "На рассмотрение"), ('approve', "Принять"), ('reject', "Отклонить"),),
        widget=forms.RadioSelect(),
    )
    rejection_reason = forms.CharField(
        label='Причина отклонения',
        required=False,
        widget=forms.Textarea(attrs={'rows': 3}),
    )

    class Meta:
        model = ReviewedOrder
        fields = ('status', 'rejection_reason')
