from django.shortcuts import HttpResponseRedirect,render
from .forms import * 
from django.conf import settings
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .business_logic import get_music_data
from django.contrib.auth import get_user_model
# Create your views here.

User = get_user_model()
def home(request):
    context={}
    if request.user.is_authenticated:
        data = get_music_data(request.user)
        context={
            "data":data,
            "authenticated":True,
            "content":settings.MEDIA_URL,
        }
    return render(request,"music_platform/home.html",context)
def root(request):
    return HttpResponseRedirect("/home/")
def registration(request):
    form=user_create()
    if request.method=="POST":
        form=user_create(request.POST)
        if User.objects.filter(email=request.POST["email"]).exists() or User.objects.filter(username=request.POST["username"]).exists():
            messages.error(request,"Email or Username Already Exists, Please use a different email")
            return HttpResponseRedirect("/registration/")
        if form.is_valid():
            form.save()
            messages.success(request,"Signed-Up Succesfully")
            return HttpResponseRedirect("/login/")
    context={
        'form':form,
    }
    return render(request,"music_platform/registration.html",context)
def logins(request):
    form=user_sign()
    if request.method=="POST":
        users=authenticate(username=request.POST["email"],password=request.POST["password"])
        if users != None:
            login(request,users)
            messages.success(request,f"Welcome {request.user.first_name}, You have Logged In Succesfully")
            return HttpResponseRedirect("/")
        else:
            messages.error(request,"Email/Password does not exist")
            return HttpResponseRedirect("/login/")
    context={
        "form":form,
        }
    return render(request,"music_platform/login.html",context)
def logouts(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request,"Successfully Logged Out")
        return HttpResponseRedirect("/login/")
    else:
        messages.error(request,"Logout failed, Not logged in")
        return HttpResponseRedirect("/login/")
    
