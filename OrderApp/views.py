from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from Product.models import Category,Product
from EcomApp.models import Setting
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.crypto import get_random_string
from UserApp.models import UserProfileModel


def Add_To_Shopping_Cart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checking = ShopCart.objects.filter(product_id=id, user_id=current_user.id)

    if checking:
        control = 1
    else:
        control = 0

    if request.method == "POST":
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control ==1:

                data = ShopCart.objects.filter(product_id=id, user_id=current_user.id)
                data.quantity += form.cleaned_data['quantity']
                data.save() 
            else:
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request,'Your Product has been added')
        return HttpResponseRedirect(url)
    else:
        if control ==1:
            data = ShopCart.objects.filter(product_id=id, user_id=current_user.id)
            data.quantity +=1
            data.save()
        else:
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        messages.success(request,'Your product has been added')
        return HttpResponseRedirect(url)

def Cart_Details(request):
    current_user = request.user
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    cart_product = ShopCart.objects.filter(user_id=current_user.id)
    total_amount = 0
    for p in cart_product:
        total_amount += p.product.new_price*p.quantity
    context = {'category':category,
               'setting':setting,
               'cart_product':cart_product,
               'total_amount':total_amount}
    return render(request,'cart_details.html',context)


def Delete_Cart_Product(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    cart_product = ShopCart.objects.filter(id=id, user_id=current_user.id)
    cart_product.delete()
    messages.warning(request,'Your product has been deleted')
    return HttpResponseRedirect(url)

@login_required(login_url='user_login/')
def OrderCart(request):

    current_user = request.user
    shoping_cart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shoping_cart:
        totalamount += rs.quantity*rs.product.new_price
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = Order()
            print("This is step1 method")
            # get product quantity from form
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.phone = form.cleaned_data['phone']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user_id = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()  # random cod
            dat.code = ordercode
            dat.save()

            # moving data shortcart to product cart
            for rs in shoping_cart:
                data = OrderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            # Now remove all oder data from the shoping cart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            # request.session['cart_item']=0
            messages.success(request, 'Your oder has been completed')
            category = Category.objects.all()
            setting = Setting.objects.get(id=1)
            context = {
                # 'category':category,
                'ordercode': ordercode,
                'category': category,
                'setting': setting,
            }

            return render(request, 'order_completed.html', context)
        else:
            messages.warning(request, form.errors)
          #  return HttpResponseRedirect("/order/oder_cart")
    form = OrderForm()
    profile = UserProfileModel.objects.get(user_id=current_user.id)
    total_amount = 0
    for p in shoping_cart:
        total_amount += p.product.new_price*p.quantity
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    print("This is step2 method")
    context = {
        # 'category':category,
        'shoping_cart': shoping_cart,
        'totalamount': totalamount,
        'profile': profile,
        'form': form,
        'category': category,
        'setting': setting,
        'total_amount': total_amount
    }
    return render(request, 'order_form.html', context)




    '''
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    totalamount = 0
    for rs in shopcart:
        totalamount += rs.quantity*rs.product.new_price
    if request.method == "POST":
        form = OrderForm(request.POST, request.FILES)
        if form.is_valid():
            dat = Order()
            dat.first_name = form.cleaned_data['first_name']
            dat.last_name = form.cleaned_data['last_name']
            dat.phone = form.cleaned_data['phone']
            dat.address = form.cleaned_data['address']
            dat.city = form.cleaned_data['city']
            dat.country = form.cleaned_data['country']
            dat.transaction_id = form.cleaned_data['transaction_id']
            dat.transaction_image = form.cleaned_data['transaction_image']
            dat.user = current_user.id
            dat.total = totalamount
            dat.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            dat.code = ordercode
            dat.save()

            for rs in shopcart:
                data = OrderProduct()
                data.order_id = dat.id
                data.product_id = rs.product_id
                data.user_id = current_user.id
                data.quantity = rs.quantity
                data.price = rs.product.new_price
                data.amount = rs.amount
                data.save()

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()
            # Now remove all oder data from the shoping cart
            ShopCart.objects.filter(user_id=current_user.id).delete()
            # request.session['cart_item']=0
            messages.success(request, 'Your oder has been completed')
            category = Category.objects.all()
            setting = Setting.objects.get(id=1)
            context = {
                # 'category':category,
                'ordercode': ordercode,
                'category': category,
                'setting': setting,
            }

            return render(request, 'order_completed.html', context)
        else:
            messages.warning(request, form.errors)
          #  return HttpResponseRedirect("/order/oder_cart")
    form = OrderForm()
    total_amount = 0
    for p in shopcart:
        total_amount += p.product.new_price*p.quantity
    profile = UserProfileModel.objects.get(user_id=current_user.id)
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    context = {
        'shopcart':shopcart,
        'totalamount':totalamount,
        'form':form,
        'profile':profile,
        'category':category,
        'setting':setting,
        'total_amount':total_amount
    }
    return render(request,'order_form.html',context) 
                    
   '''

def Order_List(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    order_list = Order.objects.filter(user_id=current_user.id)

    context = {
        'category':category,
        'setting':setting,
        'order_list':order_list,
    }
    
    return render(request,'order_showing.html',context)




         

        

