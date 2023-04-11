from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

from django.core.validators import EmailValidator, RegexValidator


class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, label=_('ФИО'))
    email = forms.EmailField(label=_('Электронная почта'), validators=[EmailValidator()])
    phone_regex = RegexValidator(
        regex=r'^\\+?[0-9]{1,3}\\s?\\(?[0-9]{3}\\)?[-.\\s]?[0-9]{3}[-.\\s]?[0-9]{4}$',
        message=_("Номер телефона должен быть в формате: '+999 (999) 999-9999'."))
    phone_number = forms.CharField(validators=[phone_regex], max_length=20, label=_('Номер телефона'))

    class Meta(UserCreationForm.Meta):
        fields = UserCreationForm.Meta.fields + ('full_name', 'email', 'phone_number')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = _('Пароль')
        self.fields['password2'].label = _('Повторите пароль')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data.get('full_name')
        user.email = self.cleaned_data.get('email')
        user.phone_number = self.cleaned_data.get('phone_number')
        if commit:
            user.save()
        return user


class CustomUserForm(CustomUserCreationForm):
    class Meta(CustomUserCreationForm.Meta):
        fields = CustomUserCreationForm.Meta.fields + ('is_active',)
