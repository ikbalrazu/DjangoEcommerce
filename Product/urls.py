from django.urls import path
from .views import Add_Comment

urlpatterns = [
    path('product-review/<int:id>/',Add_Comment,name='add_comment'),

]