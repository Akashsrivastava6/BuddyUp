from django.shortcuts import render
from core.models import following,tweets_data
import tweepy
import pandas as pd
from random import randint
from django.core.mail import send_mail
from passlib.hash import pbkdf2_sha256
from . import Preprocess


# Create your views here.

def AddFriend(request):
        if request.session.has_key('username'):
                request.session.set_expiry(180)
                usr=request.session['username']
                friend_handle=request.POST.get("twitter_handle")
                friend_email=request.POST.get("email")
                url=pbkdf2_sha256.encrypt(str(randint(1,1000)),rounds=100)
                friend_tweet=following(user_id=usr,twitter_handle=friend_handle,friend_Email=friend_email,url=url)



                send_mail("test mail","127.0.0.1:8000/oauth/login/twitter/","a.team.ucd.5@gmail.com",[friend_email])
                friend_tweet.save()

                return render(request,'submit.html',{'Message':"An Email has been sent for confirmation"})
        return render(request,'submit.html',{'Message':"Please login to continue"})
def Checking(request):
        
       
        if request.user.is_authenticated:
                user=request.user.social_auth.get(provider="twitter")
                extra=user.extra_data['access_token']['screen_name']
               
                d=following.objects.get(twitter_handle=extra)
                d.isActive=1
                d.save()
                tmp=AddFriendTweets(extra)
                return render(request,'submit.html',{'Message':tmp})


        
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

def AddFriendTweets(friend_handle):
        
        
        auth=tweepy.OAuthHandler('twVFhyS2oNaSjcUUVaYVnTBpH' ,'GlvJcYHsfeT6szx7oLuVBiWgtwAg2SCEEzhJpyUuWslooI61cn')
        auth.set_access_token('1133388205372432386-LAQstjWm6AOvIHLCgbHOHGXweivpIH','cP5toz0pmQAp2T8FCh9pOgoJ1icGYatYFivQsxAN4oM1p')
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
                
                tmp1.append(j.id)
                tmp2.append(j.created_at)
                tmp3.append(j.text)
                #tweet=tweets_data(twitter_handle=friend_handle,tweet_id=j.id,tweet_data=j.text,tweet_date=j.created_at)
                #tweet.save()
                #print(tmp)

        df=Preprocess.preprocess(tmp3)
        tmp4.append([tmp,tmp1,tmp2,df])


        return tmp4

