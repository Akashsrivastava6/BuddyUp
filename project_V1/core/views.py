from django.shortcuts import render
from core.models import following,tweets_data
import tweepy
import pandas as pd
from random import randint
from django.core.mail import send_mail
from passlib.hash import pbkdf2_sha256
from . import Preprocess
import pickle
import datetime
import json
from django.db.models import Count

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

        return render(request,'contact.html',{'Message':"An Email has been sent for confirmation"})
    return render(request,'submit.html',{'Message':"Please login to continue"})
def Checking(request):


    if request.user.is_authenticated:
        user=request.user.social_auth.get(provider="twitter")
        extra=user.extra_data['access_token']['screen_name']

        d=following.objects.get(twitter_handle=extra)
        d.isActive=1
        d.save()
        tmp=AddFriendTweets(extra)

        return render(request,'contact.html',{'Message':"Thanks for the confirmation!!"})



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

    df,ind=Preprocess.preprocess(tmp3)
    #input text
    #st=["I'm not unhappy today", "I love my country"]
    #transform our input text for prediction
    #unpickle the tfidf vectorizer
    vectorizer_new = pickle.load(open("E:/D Drive/Projects/Final/Buddyup/project_V1/core/x_result.pkl", "rb" ) )
    classifier_new = pickle.load(open("E:/D Drive/Projects/Final/Buddyup/project_V1/core/classifier.pkl", "rb" ) )
    B_ok=vectorizer_new.transform(df).toarray()
    #predict label for unseen data
    df=classifier_new.predict(B_ok)
    val=len(tmp1)+1
    for j in range(0,len(tmp1)):
        if j not in ind:
            tweet=tweets_data(twitter_handle=friend_handle,tweet_id=tmp1[j],tweet_data=tmp3[j],tweet_date=tmp2[j],class_label=df[j])
            tweet.save()


    tmp4.append([tmp,tmp1,tmp2,tmp3,df,len(tmp1)])


    return tmp4


from datetime import date, datetime


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def trend(request):
    twitter_handle=request.POST.get("friend")
    tweet_data=tweets_data.objects.filter(twitter_handle=twitter_handle)
    t_d1=tweets_data.objects.filter(twitter_handle=twitter_handle).filter(class_label=0).values('tweet_date').annotate(count=Count('tweet_date'))
    t_d2=tweets_data.objects.filter(twitter_handle=twitter_handle).filter(class_label=1).values('tweet_date').annotate(count=Count('tweet_date'))
    twt_date=[]
    twt_str = []
    for d in tweet_data:
        #  twt_date.append({'date': d.tweet_date,'tweet': d.tweet_data,'label': d.class_label})
        twt_date.append({
            "x": d.tweet_date,
            "y": d.class_label,
        })
        twt_str.append({"id": d.tweet_id, "tweets": d.tweet_data})
    chk1=[]
    chk2=[]
    for d in t_d1:
        #  twt_date.append({'date': d.tweet_date,'tweet': d.tweet_data,'label': d.class_label})
        chk1.append({"x":d['tweet_date'],"y":d['count'],'class_label':0}) 

    for d in t_d2:
        chk2.append({"x":d['tweet_date'],"y":d['count'],'class_label':1}) 

    return render(request, 'trend.html', {"Message": json.dumps(twt_date, default=json_serial), "tweet_data":twt_str, "friend": twitter_handle,'obj1':json.dumps(chk1,default=json_serial),'obj2':json.dumps(chk2,default=json_serial)})
