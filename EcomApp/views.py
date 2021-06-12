from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from EcomApp.models import Setting, ContactMessage, ContactForm
from Product.models import Category, Product, Images, CommentModel
from django.contrib import messages
from OrderApp.models import ShopCart
from .forms import SearchForm
import json

# Create your views here.
def Home(request):
    #for cart view in header start
    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price*p.quantity
    #for cart view in header end
    #for cart view in header count
    total_count = 0
    for p in cart_product:
        total_count += p.quantity

    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    sliding_image = Product.objects.all().order_by('id')[:3]
    latest_products = Product.objects.all().order_by('-id')
    context = {'setting':setting,
               'sliding_image':sliding_image,
               'latest_products':latest_products,
               'category':category,
               'cart_product':cart_product,
               'total_amount':total_amount,
               'total_count':total_count}
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
    
    current_user = request.user
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price*p.quantity


    total_count = 0
    for p in cart_product:
        total_count += p.quantity

    setting = Setting.objects.get(id=1)
    single_product = Product.objects.get(id=id)
    images = Images.objects.filter(product_id=id)
    product = Product.objects.all().order_by('id')[:4]
    category = Category.objects.all()
    comment = CommentModel.objects.filter(product_id=id, status='True')

    context = {'single_product':single_product,
               'setting':setting,
               'images':images,
               'product':product,
               'category':category,
               'comment':comment,
               'cart_product':cart_product,
               'total_amount':total_amount,
               'total_count':total_count,
               }

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

def SearchView(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            cat_id = form.cleaned_data['cat_id']
            if cat_id == 0:
                product = Product.objects.filter(title__icontains=query)
                #SELECT * FROM product WHERE title LIKE '%query%'
            else:
                product = Product.objects.filter(title__icontains=query, category_id=cat_id)
            category = Category.objects.all()
            context = {
                'category':category,
                'query':query,
                'product_cat':product
            }
            return render(request,'category_product.html',context)
    return HttpResponseRedirect('category_product')

def search_auto(request):
  if request.is_ajax():
    q = request.GET.get('term', '')
    product = Product.objects.filter(title__icontains=q)
    results = []
    for pl in product:
      product_json = {}
      product_json = pl.title
      results.append(product_json)
    data = json.dumps(results)
  else:
    data = 'fail'
  mimetype = 'application/json'
  return HttpResponse(data, mimetype)

