from django.shortcuts import render,redirect
from django.contrib.auth import logout,authenticate,login,update_session_auth_hash
from Product.models import Category
from django.contrib import messages
from EcomApp.models import Setting
from .models import UserProfileModel
from .forms import user_signup, UpdateProfileForm, UpdateUserForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


# Create your views here.
def User_Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('testing')
        # Redirect to a success page.
        
        else:
            messages.warning(request, 'Your username or password is invalid')
        # Return an 'invalid login' error message
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    context = {'category':category,
               'setting':setting}
    return render(request,'user_login.html',context)

def User_Logout(request):
    logout(request)
    return redirect('testing')


def User_Registration(request):
    if request.method == 'POST':
        form = user_signup(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password_raw = form.cleaned_data.get('password1')
            user = authenticate(username=username,password=password_raw) 
            messages.success(request, 'Your Registration successfully completed. Plz SignIn now')
            login(request,user)
            current_user = request.user
            data = UserProfileModel()
            data.user_id=current_user.id
            data.image ="user_img/IMG_20190813_024212__01.jpg"
            data.save()
            return redirect('user_login')
        else:
            messages.warning(request, 'Your password is not matching')
    else:
        form=user_signup() 
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    context = {'category':category,
               'setting':setting,
               'form':form}
    return render(request,'user_registration.html',context)

def userprofile(request):
    category = Category.objects.all()
    setting = Setting.objects.get(id=1)
    current_user = request.user
    profile = UserProfileModel.objects.get(user_id=current_user.id)

    context = {

        'category':category,
        'setting':setting,
        'profile':profile

    }
    return render(request,'user_profile.html',context)


#check login
@login_required(login_url='user_login')
def UpdateUserProfile(request):
    if request.method == 'POST':
        userform = UpdateUserForm(request.POST, instance=request.user)
        #here instance=request.user.userprofilemodel userprofilemodel asche jei model theke amra urserform korechi
        profileform = UpdateProfileForm(request.POST, request.FILES, instance=request.user.userprofilemodel)
        if userform.is_valid() and profileform.is_valid():
            userform.save()
            profileform.save()
            messages.success(request,'Your account has been updated')
            return redirect('userprofile')

    else:
        userform = UpdateUserForm(instance=request.user)
        profileform = UpdateProfileForm(instance=request.user.userprofilemodel)
        category = Category.objects.all()
        setting = Setting.objects.get(id=1)

        context = {
            'userform':userform,
            'profileform':profileform,
            'category':category,
            'setting':setting,
        }

        return render(request,'update_user_profile.html',context)

@login_required(login_url='user_login')
def user_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request,user)
            messages.success(request,'Your password was successfully updated')
            return redirect('userprofile')

        else:
            messages.error(request,'correct the error below.<br>'+str(form.errors))
            return redirect('changepassword')
    else:
        category = Category.objects.all()
        setting = Setting.objects.get(id=1)
        form = PasswordChangeForm(request.user)

        context = {
            'category':category,
            'setting':setting,
            'form':form,
        }
        return render(request,'change_password.html',context)
    


