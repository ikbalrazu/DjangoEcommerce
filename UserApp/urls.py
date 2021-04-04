from django.urls import path
from .views import User_Logout, User_Login, User_Registration,userprofile, UpdateUserProfile, user_password



urlpatterns = [

    path('user-login/',User_Login,name='user_login'),
    path('user-registration/',User_Registration, name='user_registration'),
    path('logout/',User_Logout,name='user_logout'),
    path('userprofile/',userprofile,name='userprofile'),
    path('updateuserprofile/',UpdateUserProfile,name='updateuserprofile'),
    path('change-password/',user_password,name='changepassword')
    
]