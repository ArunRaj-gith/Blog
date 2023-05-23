from django.contrib import messages
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth

from blogapp.models import blog


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password = request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('home')
        else:
            messages.info(request,"invalid details")
            return redirect('login')
    else:
        return render(request,'login.html')

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2 = request.POST['password2']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email taken')
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                print('user created')

        else:
            print('password not matched')
            return redirect('register')
        return redirect('login')

    else:
        return render(request,'login.html')

def home(request):
    return render(request,'home.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

def create(request):
    if request.method=='POST':
        topic=request.POST.get('topic')
        title = request.POST.get('title')
        img=request.FILES['img']
        desc=request.POST.get('content')
        b=blog(topic=topic,title=title,img=img,desc=desc)
        b.save()
        print('Blog added')
    return render(request,'createblog.html')

def viewblog(request):
    obj=blog.objects.all()
    return render(request,'viewblog.html',{'results':obj})

def update(request,id):
    obj=blog.objects.get(id=id)
    form=ModelForm(request.POST or None,request.FILES,instance=obj)
    if form.is_valid():
        form.save()
        return redirect('view_blog')
    return render(request,'update.html',{'form':form,'obj':obj})

def delete(request,id):
    if request.method=='POST':
        obj=blog.objects.get(id=id)
        obj.delete()
        return redirect('view_blog')
    return render(request,'delete.html')