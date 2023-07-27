from django.shortcuts import render
from django.shortcuts import render
from .models import StoreOwner
from django.shortcuts import render, redirect
from .models import StoreOwner
from django.contrib.auth.models import User
from .serializers import *
from django.contrib.auth import authenticate, login, logout
from .serializers import UserRegistrationSerializer
from django.contrib.auth.decorators import login_required
def index(request):
    return render(request, "index.html")

def storeowner(request):
    return render(request, "register_store_owners.html")

def thanku(request):
    return render(request, "thanku.html")

def error(request):
    return render(request, "error.html")

def storeuser(request):
    return render(request, "storeowner.html")
@login_required
def register_store_owner(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            name = request.POST.get('name', '')
            email = request.POST.get('email', '')
            phone_number = request.POST.get('phone_number', '')


            try:
                existing_user  = StoreOwner.objects.filter(email=email).exists() or StoreOwner.objects.filter(phone_number=phone_number).exists()
                if existing_user:
                    return render(request, 'error.html',{'message': 'User is  already registered.'})
                else:
                    raise StoreOwner.DoesNotExist
            except StoreOwner.DoesNotExist:
                pass


            user_profile = StoreOwner(name=name, email=email, phone_number=phone_number, user=request.user)
            user_profile.save()
            return redirect('success_page') 

        return render(request, 'register_store_owners.html')
    return redirect('index' )



def view_registered_store_owners(request):
    if request.user.is_authenticated:
        salesperson = request.user
        registered_store_owners = StoreOwner.objects.filter(user=salesperson)
        return render(request, 'storeowner.html', {'registered_store_owners': registered_store_owners})
    return redirect('index')


def saleslogin(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.POST)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'error.html')
        
        if user:
            authenticated_user = authenticate(username=user.username, password=password)
            if authenticated_user is not None:
                login(request, authenticated_user)
                return redirect('register_store_owner')

    return redirect('index')

            



def salesregister(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            serializer = UserRegistrationSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
                return redirect('saleslogin.html') 

        return render(request, 'registersalesperson.html')
    return redirect('saleslogin')

def saleslogout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('sales_login')