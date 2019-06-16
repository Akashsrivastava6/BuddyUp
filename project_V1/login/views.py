from django.shortcuts import render
from login.models import User_detail,Registration
from passlib.hash import pbkdf2_sha256
import tweepy
import pandas as pd

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
    return render(request,'index.html',{"Message":"Logout Successful!"})


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


    user_login_details=User_detail(username=usr,password=pwd)
    
    user_registration_details=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob)
    user_login_details.save()
    user_registration_details.save()
    
    return render(request,'submit.html',{'Message':'You Have been Registered'})
    
def AddFriend(request):

    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        friend_handle=request.POST.get("username")

        auth=tweepy.OAuthHandler('twVFhyS2oNaSjcUUVaYVnTBpH' ,'GlvJcYHsfeT6szx7oLuVBiWgtwAg2SCEEzhJpyUuWslooI61cn')
        auth.set_access_token('1133388205372432386-vrZBcTKbtOtmqNNWJy5w9OogwNwP2g','4h53Ab15IJRopkHnnIi68E2JBdqvOZA0OMXyN3B9NAOub')
        api=tweepy.API(auth)
        public_tweets=api.user_timeline(friend_handle,count=1000)
#print(public_tweets.name)
        tmp=[]
        tmp1=[]
        tmp2=[]
        tmp3=[]
        tmp4=[]
#tweets_for_csv=for tweet in public_tweets

        for j in public_tweets:
            tmp.append(usr)
            tmp1.append(j.id)
            tmp2.append(j.created_at)
            tmp3.append(j.text)
            tmp4.append([friend_handle,j.id,j.created_at,j.text])




        return render(request,'submit.html',{'Message':"","tweets_handle":tmp,"id":tmp1,"created_at":tmp2,"text":tmp3,"tmp":tmp4})
    return render(request,'index.html')
    