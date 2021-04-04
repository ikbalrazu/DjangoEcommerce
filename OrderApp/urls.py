from django.urls import path
from .views import Add_To_Shopping_Cart, Cart_Details, Delete_Cart_Product

urlpatterns = [

    path('addingcart/<int:id>/',Add_To_Shopping_Cart, name='add_to_shopping_cart'),
    path('cart-details/',Cart_Details,name='cart_details'),
    path('delete-cart-product/<int:id>/',Delete_Cart_Product, name='cart_delete'),

]
