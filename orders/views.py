from django.shortcuts import render

def under_construction(request, *args, **kwargs):
    return render(request, 'orders/under_construction.html')

def index(request):
    context = {
        # Здесь можно добавить данные, которые будут переданы в шаблон
    }
    return render(request, 'orders/index.html', context)
