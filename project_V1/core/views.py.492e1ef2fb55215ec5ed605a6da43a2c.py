from django.shortcuts import render
from core.models import following,tweets_data
import tweepy
import pandas as pd
from random import randint
from django.core.mail import send_mail
from passlib.hash import pbkdf2_sha256
from . import Preprocess
import pickle

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

        df,ind=Preprocess.preprocess(tmp3)
        #input text
        #st=["I'm not unhappy today", "I love my country"]
        #transform our input text for prediction
        #unpickle the tfidf vectorizer
        vectorizer_new = pickle.load(open("E:/ucd/Final project/project_V1/core/x_result.pkl", "rb" ) )
        classifier_new = pickle.load(open("E:/ucd/Final project/project_V1/core/classifier.pkl", "rb" ) )
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



t=[" Wake up with determination. Go to bed with satisfaction ","It is such a  wonderful day today. Bright sunshine,loving it","Being #Grateful for small things helps us be #Humble and #Positive. What little things for you today?","It will be rainy tomorrow but it was a beautiful sunny day today."," Imagination encircles the entire world.","See, I am making all things new.--Revelation 21:5 #newbeginnings #spiritual #inspiration","Love LIFE and it will return the favor."," Be happy. Not because everything is perfect, but because you can see good in everything."," It hurts so much when you feel yourself become less, and less important to the person who means the most to you..","Everyday is a struggle lately."," Don't Fall in Love, Rise In Love! - Gurudev @SriSri Ravi Shankar","The peace that comes with surrendered action turns to a sense of aliveness when you actually enjoy what you are doing.","Be a source of strength and courage. Share your wisdom. Radiate love.","Always fun to go outside and see what nature reveals #nature","fair is foul and foul is fair hover through the fog and filthy air","I am mad for no reason"," I book a flight @Wakanowdotcom  on the 19th June 2019 after been debited successfully they did not confirm my flight order","I am so damn sick of my parents and grandparents making homophobic comments out of nowhere. Makes my blood boil. #angry","Hit me in the feels. This is why my PTSD wont let me work."]