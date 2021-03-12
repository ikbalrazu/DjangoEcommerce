from django.urls import path
from .views import Add_To_Shopping_Cart

urlpatterns = [

    path('addingcart/<int:id>/',Add_To_Shopping_Cart, name='add_to_shopping_cart'),

]
