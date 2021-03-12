from django.urls import path
from .views import Home, Single_Product, category_product, Aboutus, Contact

urlpatterns =[
    path('',Home,name='testing'),
    path('aboutus',Aboutus,name='aboutus'),
    path('contact',Contact,name='contact_dat'),
    path('single_product/<int:id>/',Single_Product,name="product_single"),
    path('category_product/<int:id>/<slug:slug>',category_product,name="category_product"),
]