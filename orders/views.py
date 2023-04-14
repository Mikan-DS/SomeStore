from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Sum
from django.shortcuts import get_object_or_404, render
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone

from .forms import CustomUserCreationForm
from .forms import ProductForm
from .models import Order
from .models import Product, ReviewedOrder


@login_required
@staff_member_required
def moderate_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    total_price = order.products.aggregate(total=Sum('price'))['total']

    if request.method == 'POST':
        reviewed_order = ReviewedOrder.objects.filter(order=order).first()

        if reviewed_order:
            ReviewedOrder.objects.filter(order=order).delete()
        status = request.POST.get('status')
        if status == 'review':
            if reviewed_order:
                reviewed_order.delete()
                reviewed_order = None
        elif status == 'accept':
            admin_user = request.user
            decision_date = timezone.now()
            rejection_reason = None
            if reviewed_order is None:
                reviewed_order = ReviewedOrder.objects.create(order=order, admin_user=admin_user,
                                                              decision_date=decision_date,
                                                              rejection_reason=rejection_reason)
            else:
                reviewed_order.admin_user = admin_user
                reviewed_order.decision_date = decision_date
                reviewed_order.rejection_reason = rejection_reason
                reviewed_order.save()
        elif status == 'reject':
            reviewed_order = ReviewedOrder.objects.filter(order=order).first()
            if reviewed_order is None:
                reviewed_order = ReviewedOrder.objects.create(order=order, admin_user=request.user,
                                                              decision_date=timezone.now())
            reviewed_order.rejection_reason = request.POST.get('reason', '')
            reviewed_order.save()
    else:
        reviewed_order = ReviewedOrder.objects.filter(order=order).first()
    context = {
        'order': order,
        'total_price': total_price,
        'reviewed_order': reviewed_order,
    }

    return render(request, 'orders/moderate_order.html', context)


@login_required
@staff_member_required
def all_orders(request):
    orders = Order.objects.filter(saved_date__isnull=False).order_by('-saved_date')
    for order in orders:
        order.total_price = order.products.aggregate(total=Sum('price'))['total']
    context = {
        'orders': orders,
    }
    return render(request, 'orders/all_orders.html', context)


@login_required
@staff_member_required
def moderate_orders(request):
    orders = Order.objects.filter(saved_date__isnull=False, reviewed_order__isnull=True).order_by('-saved_date')
    for order in orders:
        order.total_price = order.products.aggregate(total=Sum('price'))['total']
    context = {
        'orders': orders,
    }
    return render(request, 'orders/moderate_orders.html', context)


@login_required
@staff_member_required
def archive_orders(request):
    orders = Order.objects.filter(saved_date__isnull=False, reviewed_order__isnull=False).order_by('-saved_date')
    for order in orders:
        order.total_price = order.products.aggregate(total=Sum('price'))['total']
    context = {
        'orders': orders,
    }
    return render(request, 'orders/archive_orders.html', context)


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    total_price = order.products.aggregate(total=Sum('price'))['total']
    context = {
        'order': order,
        'total_price': total_price,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user, saved_date__isnull=False).order_by('-saved_date')

    for order in orders:
        order.total_price = order.products.aggregate(total=Sum('price'))['total']
    return render(request, 'orders/my_orders.html', {'orders': orders})


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
        elif request.POST.get("url") and len(request.POST.get("url")) > 199:
            messages.error(request, 'Ссылка на товар слишком длинная')
        else:
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
    if request.method == 'POST':
        order.comment = request.POST.get('comment')
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
