from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.utils import timezone

from .forms import CustomUserCreationForm

from django.contrib.auth.decorators import login_required
from .models import Order, Product
from .forms import ProductForm

@login_required
def cart(request):
    order, created = Order.objects.get_or_create(user=request.user, saved_date=None)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.order = order
            product.save()
            messages.success(request, 'Товар успешно добавлен в корзину!')
            return redirect('cart')
        elif request.POST.get("url") and len(request.POST.get("url"))>199:
            messages.error(request, 'Ссылка на товар слишком длинная')
        else:
            messages.error(request, 'Произошла ошибка при добавлении. Проверьте поля')
            form.add_error(None, 'Произошла ошибка при добавлении. Проверьте поля')
    else:
        form = ProductForm()
    context = {
        'products': order.products.all(),
        'form': form,
    }
    return render(request, 'orders/cart.html', context)

@login_required
def remove_from_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    return redirect('cart')

@login_required
def place_order(request):
    order = Order.objects.filter(user=request.user, saved_date=None).first()
    if order is None or order.products.count() == 0:
        return redirect('cart')
    order.saved_date = timezone.now()
    order.save()
    return redirect('index')


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = AuthenticationForm()
    return render(request, 'orders/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(request, username=username, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'orders/register.html', {'form': form})

def under_construction(request, *args, **kwargs):
    return render(request, 'orders/under_construction.html')

def index(request):
    return render(request, 'orders/index.html')
