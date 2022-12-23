from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
import cloudinary.uploader 
from .models import TextModel
from django.http import *

# Create your views here.
def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        try:
            target_file = request.FILES['targetfile']
            resp = cloudinary.uploader.upload(target_file)
            file_name = target_file.name
            file_link = resp.get('url')
            user = request.user
            TextModel.objects.create(text="demo",file_name=file_name,file_link=file_link,user=user)
            return redirect('home')
        except Exception as e:
            print(e)
    return render(request,"home.html")

    context = {}
    user = request.user
    textdata_list = TextModel.objects.filter(user=user)
    context['textData'] = textdata_list

    return render(request,"home.html",context=context)


def login(request):
    if request.method == "POST":
        data = request.POST
        username = data['username']
        password = data['password']

        user = authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            return redirect("home")
        else:
            HttpResponse("Invalid Credentials")
    return render(request,"login.html")


def signup(request):
    if request.method == "POST":
        data = request.POST
        name = data['name']
        username = data['username']
        password = data['password']
        confirm_password = data['confirm_password']

        user = User.objects.filter(username=username).exists()
        if not user :
            if password == confirm_password:
                user = User.objects.create_user(username=username,password=password,first_name=name)
                return redirect("login")
            else:
                return HttpResponse("Password does not match")
        else:
            return HttpResponse("username already exist")

    return render(request,"signup.html")

def logout(request):
    auth_logout(request)
    return redirect("login")

        
    