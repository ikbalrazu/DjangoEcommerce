from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .models import ShopCart, ShopCartForm

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
        return HttpResponseRedirect(url)

         

        

