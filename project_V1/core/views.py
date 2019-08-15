from django.shortcuts import render,redirect
from core.models import following,tweets_data
from login.models import User_detail,Registration
from django.core.mail import send_mail
from django.contrib.auth.models import User
import login.task
#import pandas as pd
from random import randint
from passlib.hash import pbkdf2_sha256
from django.contrib.auth import logout
import core.task
import login.task
import datetime
# Create your views here.



# method to add friend twitter handle
def AddFriend(request):
    if request.session.has_key('username'):
        request.session.set_expiry(180) # Updating session
        usr=request.session['username'] # 
        friend_handle=request.POST.get("twitter_handle") # retrieving twitter_handle
        friend_email=request.POST.get("email") # retrieving email
        if friend_handle!=None and friend_email!=None:
                url=pbkdf2_sha256.encrypt(str(randint(1,1000)),rounds=100)
                t_handle,t_handle2,msg=core.task.sendRequest(usr,friend_handle,friend_email,url) # method to send mail request to friend
                fname=login.task.getFirstName(usr) # retrieving user's name
                return render(request,'dashboard.html',{'Message':fname,'data':t_handle,'data2':t_handle2,'msg':msg}) # returing dashboard page and data
        else:
                return redirect("/login?Message=Session expired")                    
    return redirect("/login?Message=Session expired") #if the user is not logged in or session is expired

# method called when the user logs in by twitter for the first time
def Checkingtwitter(request):
        # 
        # updating session
        usr=request.GET.get("twitter_handle")
        request.session['username']=usr 
        
        email=request.POST.get("username")  
        pwd=request.POST.get('password')
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        dob=request.POST.get("dob")
        pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000) # encrypting password
        d1=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob) # Registring the user 
        d1.save() # 
        d=User_detail.objects.filter(username=usr).update(email=email) # updating users email
        d=User_detail.objects.filter(username=usr).update(password=pwd) # updating users password
        
        page,t_handle,t_handle2,n=core.task.twitterCheck(usr.lower()) # calling twittercheck
        request.session.set_expiry(n)
        fname=login.task.getFirstName(usr) # retrieving users first name
        return render(request,page,{"Message":fname,'data':t_handle,"data2":t_handle2}) # returning page and data
       

# method used when user signin from twitter
def Checking(request):
        if request.user.is_authenticated: # if the user is authenticated
                user=request.user # retrieving authenticated user handle
                extra=str(user) # 
                u=User.objects.get(username=user) 
                u.delete()
                
                request.session['username']=extra # updating session
              
                page,t_handle,t_handle2,n=core.task.twitterCheck(extra)  # calling twittercheck
                request.session.set_expiry(n) # updating session
                # fname=login.task.getFirstName(extra)
                fname=extra   
                return render(request,page,{"Message":fname,'data':t_handle,"data2":t_handle2}) # returing page and data
        return redirect("/login") # redireting to login page if user is not redirected


# method to  get the followers list  to grant and revoke access and return follower page
def Followers(request):
        if request.session.has_key('username'): # if the user is logged in then following code is executed
                request.session.set_expiry(180) # updating session
                usr=request.session['username'] #retrieving logged in user
                friend=request.POST.get("friend")
                status=request.POST.get("status")
                if status=="Grant": 
                        d=following.objects.filter(twitter_handle=usr).filter(user_id=friend).update(isActive=1) # granting access to a particular friend
                        handle_data=tweets_data.objects.filter(twitter_handle=usr) 
                        if len(handle_data)==0: # checking if the data for the twiteer handle is in database. If not then adding tweets data db. 
                                tmp=core.task.AddFriendTweets.delay(str(usr)) 
                elif status=="Revoke":
                        emails=User_detail.objects.filter(username=friend)
                        d=following.objects.filter(twitter_handle=usr).filter(user_id=friend).delete() # if the status is Revoke then revoking access for that particular friend.
                        
                        for email in emails:
                                send_mail("Access revoked by @"+usr,"Your friend just @"+usr +" revoked the access. To access his twitter timeline please add him again.","a.team.ucd.5@gmail.com",[email.email]) # sending mail to the friend
                t_handle=core.task.getFollower(usr) # retrieving followers list from db
                noti_list, dd1=login.task.notificationdata(usr) # retrieving notification data from db
                fname=login.task.getFirstName(usr) # retrieving first name of the logged in user
                return render(request,'followers.html',{'Message':fname,'data':t_handle,'noti':noti_list,'dd1':dd1}) # returning page and data

        return redirect("/login") # i fthe user is not logged in then redirected to login page.


# method to get trend page
def trend(request):
    if request.session.has_key('username'): # if the user is logged in then following code is exceuted
        request.session.set_expiry(180) # updating session
        usr=request.session['username'] # retrieving logged in user
        twitter_handle=request.POST.get("friend") # retrieving the friend for which trend button is clicked
        if twitter_handle!=None:
                message,tweet_data,friend,obj1,obj2,summ=core.task.getTrend(twitter_handle) # get trend method is called to get the trend data from db
                fname=login.task.getFirstName(usr) # retrieving the logged in user friest name
                sumry=""
                if summ >0.5 and summ <5:
                        sumry="Positive"
                elif summ==101:
                        sumry="No"
                elif summ<=0.5 and summ>=-0.5:
                        sumry="Neutral"
                elif summ<-0.5 and summ >-5:
                        sumry="Negative"
                return render(request, 'trend.html', {"usr":fname,"Message": message, "tweet_data":tweet_data, "friend": friend,'obj1':obj1,'obj2':obj2,"summ":sumry}) # returning page and data 
        else:
                return redirect("/login") 
    else:
        return redirect("/login") # if the user is not logged in or session is expired.