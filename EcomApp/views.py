from django.shortcuts import render
from django.http import HttpResponse
from EcomApp.models import Setting
from Product.models import Category, Product

# Create your views here.
def Home(request):
    setting = Setting.objects.get(id=1)
    sliding_image = Product.objects.all().order_by('id')[:3]
    latest_product = Product.objects.all().order_by('-id')
    context = {'setting':setting,
               'sliding_image':sliding_image,
               'latest_product':latest_product}
    print(context)
    return render(request,'home.html',context)
