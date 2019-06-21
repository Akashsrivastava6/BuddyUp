from django.shortcuts import render,redirect
from login.models import User_detail,Registration
from passlib.hash import pbkdf2_sha256
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'index.html')

# Create your views here.
def loginPage(request):
    if request.session.has_key('username'):
        request.session.set_expiry(180)
        return render(request,'addfriend.html',{'Message':"welcome :"+request.session['username']})
    return render(request,'index.html')

def logoutRequest(request):
    try:
        del request.session['username']
        
    except KeyError:
        pass
   # return render(request,'index.html',{"Message":"Logout Successful!"})
    return redirect("/login")


def signupUser(request):
    return render(request,'signup.html')


def loginRequest(request):

    if request.session.has_key('username'):
        request.session.set_expiry(180)
        return render(request,'addfriend.html',{'Message':"welcome :"+request.session['username']})
    request.session.clear_expired()

    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    if usr==None:
        return render(request,'index.html',{'Message':"Please enter Username"})
    if pwd==None:
        return render(request,'index.html',{'Message':"Please enter Password"})
    try:
        data=User_detail.objects.get(username=usr)
    except:
        return render(request,'index.html',{'Message':"Username not registered!"})
    if pbkdf2_sha256.verify(pwd,data.password):
        request.session.set_expiry(180)
        request.session['username']=usr
        return render(request,'addfriend.html',{'Message':"welcome :"+data.username})
    else:
        return render(request,'index.html',{'Message':"Incorrect Password!"})

def RegisterUser(request):
    
    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    dob=request.POST.get("dob")
    pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000)

    try:
        data=User_detail.objects.get(username=usr)
    except:
        
        user_login_details=User_detail(username=usr,password=pwd)
        
        user_registration_details=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob)
        user_login_details.save()
        user_registration_details.save()
        
        return render(request,'signup.html',{'Message':"You have been registered!!"})
    return render(request,'signup.html',{'Message':"Email already registered"})    

    