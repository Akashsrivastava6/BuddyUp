from django.shortcuts import render,redirect
from core.models import following,tweets_data
from login.models import User_detail,Registration
from django.contrib.auth.models import User
import login.task
#import pandas as pd
from random import randint
from passlib.hash import pbkdf2_sha256
from django.contrib.auth import logout
import core.task
import datetime
# Create your views here.

def AddFriend(request):
    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        friend_handle=request.POST.get("twitter_handle")
        friend_email=request.POST.get("email")
        if friend_handle!=None and friend_email!=None:
                url=pbkdf2_sha256.encrypt(str(randint(1,1000)),rounds=100)
                t_handle,msg=core.task.sendRequest(usr,friend_handle,friend_email,url)
                return render(request,'dashboard.html',{'Message':request.session['username'],'data':t_handle,'msg':msg})
        else:
                return redirect("/login?Message=Session expired")                    
    return redirect("/login?Message=Session expired")


def Checking(request):
        if request.user.is_authenticated:
                user=request.user#.social_auth.get(provider="twitter")
                extra=user#.extra_data['access_token']['screen_name']
                u=User.objects.get(username=user)
                u.delete()
                request.session.set_expiry(180)
                request.session['username']=extra
                page,t_handle=core.task.twitterCheck(extra)

                return render(request,page,{"Message":request.session['username'],'data':t_handle})

                # d1=User_detail.objects.filter(username=extra)
                # if len(d1)>0:
                #         userfollowing=following.objects.filter(twitter_handle=extra)
                #         if len(userfollowing)>0:
                #                 if len(userfollowing.filter(isActive=1))>0:
                #                         request.session.set_expiry(180)
                #                         request.session['username']=extra
                #                         t_handle=login.task.getFriends(extra)
                #                         return render(request,'dashboard.html',{'Message': request.session['username'],'data':t_handle})
                
                #                 else:
                #                         request.session.set_expiry(180)
                #                         request.session['username']=extra
                #                         t_handle=core.task.getFollower(extra)
                #                         return render(request,'followers.html',{'Message': rrequest.session['username'],'data':t_handle})
                #         else:
                #                 request.session.set_expiry(180)
                #                 request.session['username']=extra
                #                 t_handle=login.task.getFriends(extra)
                #                 return render(request,'dashboard.html',{'Message':request.session['username'],'data':t_handle})
                
                # else:
                        
                #         adduserD=User_detail(username=extra)
                # # adduserR=Registration(username_id=extra,firstname=userdata.first_name,lastname=userdata.last_name)
                #         adduserD.save()
                #         #adduserR.save()

                #         userfollowing=following.objects.filter(twitter_handle=extra)
                #         if len(userfollowing)>0:
                #                 if len(userfollowing.filter(isActive=1))>0:
                #                         request.session.set_expiry(180)
                #                         request.session['username']=extra
                #                         t_handle=login.task.getFriends(extra)
                #                         return render(request,'dashboard.html',{'Message':request.session['username'],'data':t_handle})
                
                #                 else:
                #                         request.session.set_expiry(180)
                #                         request.session['username']=extra
                #                         t_handle=core.task.getFollower(extra)
                #                         return render(request,'followers.html',{'Message':request.session['username'],'data':t_handle})
                #         else:
                #                 request.session.set_expiry(180)
                #                 request.session['username']=extra
                #                 t_handle=login.task.getFriends(extra)
                #                 return render(request,'dashboard.html',{'Message':request.session['username'],'data':t_handle})
                
                        
                # d=following.objects.get(twitter_handle=extra)
                # d.isActive=1
                # d.save()
                # tmp=core.task.AddFriendTweets.delay(extra)

        return redirect("/login")



def Followers(request):
        if request.session.has_key('username'):
                request.session.set_expiry(180)
                usr=request.session['username']
                friend=request.POST.get("friend")
                status=request.POST.get("status")
                if status=="Grant":
                        d=following.objects.filter(twitter_handle=usr).filter(user_id=friend).update(isActive=1)
                        tmp=core.task.AddFriendTweets.delay(str(usr))
                else:
                        d=following.objects.filter(twitter_handle=usr).filter(user_id=friend).update(isActive=0)

                t_handle=core.task.getFollower(usr)
                return render(request,'followers.html',{'Message':request.session['username'],'data':t_handle})

        return redirect("/login")

'''
def VerifyFriend(request):
        usr=request.GET.get("usr")
        friend_handle=request.GET.get("friend_handle")
        friend_email=request.GET.get("friend_email")
        url=request.GET.get("url")
        d=following.objects.get(url=url)
        
        d.isActive=1
        d.save()


        tmp=AddFriendTweets(friend_handle)
                

        print(tmp)
        
        return render(request,'submit.html',{'Message':friend_handle})


'''

def trend(request):
    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        twitter_handle=request.POST.get("friend")
        if twitter_handle!=None:
                message,tweet_data,friend,obj1,obj2=core.task.getTrend(twitter_handle)
                return render(request, 'trend.html', {"usr":usr,"Message": message, "tweet_data":tweet_data, "friend": friend,'obj1':obj1,'obj2':obj2})
        else:
                return redirect("/login")        
    else:
        return redirect("/login")