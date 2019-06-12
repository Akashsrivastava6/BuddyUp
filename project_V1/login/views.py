from django.shortcuts import render
from login.models import User_detail,Registration
from passlib.hash import pbkdf2_sha256
# Create your views here.
def loginPage(request):
    if request.session.has_key('username'):
        request.session.set_expiry(180)
        return render(request,'submit.html',{'Message':"welcome :"+request.session['username']})
    return render(request,'index.html')


def signupUser(request):
    return render(request,'signup.html')


def loginRequest(request):

    
    request.session.clear_expired()

    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    if usr==None:
        return render(request,'submit.html',{'Message':"You are not logged in"})
    try:
        data=User_detail.objects.get(username=usr)
    except:
        return render(request,'submit.html',{'Message':"username not registered yet"})
    if pbkdf2_sha256.verify(pwd,data.password):
        request.session.set_expiry(180)
        request.session['username']=usr
        return render(request,'submit.html',{'Message':"welcome :"+data.username})
    else:
        return render(request,'submit.html',{'Message':"password is incorrect"})

def RegisterUser(request):
    
    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    dob=request.POST.get("dob")
    pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000)


    user_login_details=User_detail(username=usr,password=pwd)
    
    user_registration_details=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob)
    user_login_details.save()
    user_registration_details.save()
    
    return render(request,'submit.html',{'Message':'You Have been Registered'})
    
