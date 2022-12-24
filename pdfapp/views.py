from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
import cloudinary.uploader 
from .models import TextModel
from django.http import *
from django.contrib import messages
import requests

import io
from PIL import Image
import pytesseract
from wand.image import Image as wi
from pdf2image import convert_from_bytes

# Create your views here.
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe" 

def ocr(target_file):
    if target_file.content_type == 'application/pdf':
        images = convert_from_bytes(request_file,500,poppler_path="C:\Program Files\poppler-22.12.0\Library\\bin")
        for image in images:
            text = pytesseract.image_to_string(image, lang = 'eng')
    else:
        image = Image.open(io.BytesIO(request_file))
        text = pytesseract.image_to_string(image, lang = 'eng')
    print(text)
    return text

def home(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        try:
            target_file = request.FILES['target_file']
            resp = cloudinary.uploader.upload(target_file )
            print(resp)
            file_name = target_file.name
            file_link = resp.get('url')
            user = request.user
            text = ocr(target_file)
            TextModel.objects.create(text=text,file_name=file_name,file_link=file_link,user=user)
            return redirect('home')
        except Exception as e:
            print(e)
            messages.error(request, 'Unable to process request, Try again')
            redirect("home") 

    context = {}
    user = request.user
    textdata_list = TextModel.objects.filter(user=user)
    context['textData'] = textdata_list

    return render(request,"home.html",context=context)

def text(request,pk):
    if request.user.is_authenticated:
        textObj = TextModel.objects.filter(pk=pk,user=request.user).first()
        if textObj is None:
            return HttpResponse('Access Denied', status=403)
        context = {}
        context['singleTextData'] = textObj.text
        return render(request,'text.html',context)
        # template = "<pre>" + textObj.text + "</pre>"
    else:
        return HttpResponse('Unauthorized', status=401)

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
            messages.error(request,"Invalid Credentials")
            return redirect('login')
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
                messages.error(request,"Password does not match")
                return redirect('signup')
        else:
            messages.error(request, "Username already exist")
            return redirect('signup')

    return render(request,"signup.html")

def logout(request):
    auth_logout(request)
    return redirect("login")

        
    