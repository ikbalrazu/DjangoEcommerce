from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from EcomApp.models import Setting, ContactMessage, ContactForm
from Product.models import Category, Product, Images
from django.contrib import messages

# Create your views here.
def Home(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    sliding_image = Product.objects.all().order_by('id')[:3]
    latest_products = Product.objects.all().order_by('-id')
    context = {'setting':setting,
               'sliding_image':sliding_image,
               'latest_products':latest_products,
               'category':category}
    print(context)
    return render(request,'home.html',context)

def Aboutus(request):
    category = Category.objects.all()
    context = {'category':category}
    return render(request,'about.html',context)


def Contact(request):
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            data = ContactMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request,'Your message has been submited')
            return HttpResponseRedirect(request('contact_dat'))

    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    form = ContactForm
    context = {
        'setting':setting, 'form':form, 'category':category
    }
    return render(request,'contact_form.html',context)


def Single_Product(request,id):
    
    setting = Setting.objects.get(id=1)
    single_product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)
    product = Product.objects.all().order_by('id')[:4]
    category = Category.objects.all()

    context = {'single_product':single_product,
               'setting':setting,
               'images':images,
               'product':product,
               'category':category}

    return render(request,'product_single.html',context) 

def category_product(request,id,slug):
    setting = Setting.objects.get(id=1)
    category = Category.objects.all()
    product_cat = Product.objects.filter(category_id=id)
    sliding_image = Product.objects.all().order_by('id')[:3]

    context = {'product_cat':product_cat,
               'setting':setting,
               'category':category,
               'sliding_image':sliding_image}

    return render(request,'category_product.html',context)