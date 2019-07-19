from django.db.models import Count,Max
from celery.decorators import task,periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from core.models import following,tweets_data
from login.models import User_detail,Registration
import login.task
import json
import datetime
from datetime import date, datetime
import tweepy
from . import Preprocess
import pickle
import pandas as pd


def sendRequest(usr,friend_handle,friend_email,url):
    t_handle=login.task.getFriends(usr) 
    data=following.objects.filter(user_id=usr).filter(twitter_handle=friend_handle)
    if len(data)>0:
        
        return t_handle,"Request already send for this twitter handle."
    else:
        friend_tweet=following(user_id=usr,twitter_handle=friend_handle,friend_Email=friend_email,url=url)
        send_mail("test mail","127.0.0.1:8000/oauth/login/twitter/","a.team.ucd.5@gmail.com",[friend_email])
        friend_tweet.save()
        return t_handle,"An Email is send for Confirmation!"
        



def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def getFollower(user):
    data3=following.objects.filter(twitter_handle=user)
    followed=[]
    
    for d in data3:
        user=""
        # try:
        #     data=Registration.objects.get(username_id =d.user_id)
        
        #     user=data.FirstName+data.LastName
            
        # except:
        user=d.user_id
        if d.isActive==0:
           followed.append({"user":user,"status":"Grant Access"})
        else:
            followed.append({"user":user,"status":"Revoke Access"})
    return followed

def getTrend(twitter_handle):
    tweet_data=tweets_data.objects.filter(twitter_handle=twitter_handle)
    
    # USed for mvp
    '''
    t_d1=tweets_data.objects.filter(twitter_handle=twitter_handle)..values('tweet_date').annotate(count=Count('tweet_date'))
    t_d2=tweets_data.objects.filter(twitter_handle=twitter_handle).filter(class_label=1).values('tweet_date').annotate(count=Count('tweet_date'))
    twt_date=[]
    twt_str = []
    for d in tweet_data:
        #  twt_date.append({'date': d.tweet_date,'tweet': d.tweet_data,'label': d.class_label})
        twt_date.append({
            "x": d.tweet_date,
            "y": d.class_label,
        })
        if(d.class_label==0):
            twt_str.append({"id": d.tweet_date, "tweets": d.tweet_data,'class':"Negative"})
        else:
            twt_str.append({"id": d.tweet_date, "tweets": d.tweet_data,'class':"Positive"})
    chk1=[]
    chk2=[]
    for d in t_d1:
        #  twt_date.append({'date': d.tweet_date,'tweet': d.tweet_data,'label': d.class_label})
        chk1.append({"x":d['tweet_date'],"y":d['count'],'class_label':0}) 
    for d in t_d2:
        chk2.append({"x":d['tweet_date'],"y":d['count'],'class_label':1}) 
    '''
    t_d1=tweets_data.objects.filter(twitter_handle=twitter_handle).values('tweet_date').distinct()
    f = "YY-MM-DD"
    twt_date=[]
    tweet=[]
    date=[]
    scores=[]
    for a in range(len(t_d1)):
        t_d2=tweets_data.objects.filter(twitter_handle=twitter_handle).filter(tweet_date=t_d1[a]['tweet_date'])
        
        score=0
        counter=0
        
       

        for d in t_d2:
            tweet.append(d.tweet_data)
            date.append(d.tweet_date)
            scores.append(d.score)
            score=score+d.score
            counter=counter+d.counter
        if counter!=0:
            twt_date.append({"date":t_d1[a]['tweet_date'],"score":(score/counter)})
        else:
            twt_date.append({"date":t_d1[a]['tweet_date'],"score":0})
        df=pd.DataFrame(tweet,columns=['Tweet'])
        df['Date']=date
        df['Score']=scores        
        df.to_csv("C:/Users/arnab/OneDrive/Documents/GitHub/testlist1.csv", encoding='utf-8-sig')
    return json.dumps(twt_date, default=json_serial),twt_date,twitter_handle,json.dumps(twt_date,default=json_serial),json.dumps(twt_date,default=json_serial)


def twitterCheck(username):
    d1=User_detail.objects.filter(username=username)
    if len(d1)>0:
        userfollowing=following.objects.filter(twitter_handle=username)
        if len(userfollowing)>0:
            if len(userfollowing.filter(isActive=1))>0:
                t_handle=login.task.getFriends(username)
                return 'dashboard.html',t_handle
            else:
                t_handle=getFollower(username)
                return 'followers.html',t_handle
        else:
            t_handle=login.task.getFriends(username)
            return 'dashboard.html',t_handle       
    else:                
        adduserD=User_detail(username=username)
        # adduserR=Registration(username_id=extra,firstname=userdata.first_name,lastname=userdata.last_name)
        
        adduserD.save()
        return 'editprofile.html',None
        #adduserR.save()
        userfollowing=following.objects.filter(twitter_handle=username)
        if len(userfollowing)>0:
            if len(userfollowing.filter(isActive=1))>0:             
                t_handle=login.task.getFriends(username)
                return 'dashboard.html''data',t_handle
            else:
                t_handle=getFollower(username)
                return 'followers.html',t_handle
        else:
            t_handle=login.task.getFriends(username)
            return 'dashboard.html',t_handle
                






@periodic_task(run_every=(crontab(minute='*/10')), name="AddTweets_task", ignore_result=True)
def AddTweets():
    data=following.objects.filter(isActive=1)
    
    for d in data:
        t_handle=d.twitter_handle
        maxid=tweets_data.objects.filter(twitter_handle=t_handle).aggregate(Max('tweet_id'))    
        auth=tweepy.OAuthHandler('twVFhyS2oNaSjcUUVaYVnTBpH' ,'GlvJcYHsfeT6szx7oLuVBiWgtwAg2SCEEzhJpyUuWslooI61cn')
        auth.set_access_token('1133388205372432386-zKJMvfgPa1hI5zGQgsWH7LOKBdk0wU','KYAQDWhALWNQcCF2URWtgoXNzjZkRiBueIlBGj26nQcld')
        api=tweepy.API(auth)
        public_tweets=api.user_timeline(t_handle,since_id=str(maxid['tweet_id__max']),count=1000,tweet_mode='extended')
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
            tmp3.append(j.full_text)
            #tweet=tweets_data(twitter_handle=friend_handle,tweet_id=j.id,tweet_data=j.text,tweet_date=j.created_at)
            #tweet.save()
            #print(tmp)
        if len(tmp3)>0:
            # for mvp
            '''
            df,ind=Preprocess.preprocess(tmp3)
            #input text
            #st=["I'm not unhappy today", "I love my country"]
            #transform our input text for prediction
            #unpickle the tfidf vectorizer
            vectorizer_new = pickle.load(open("C:/Users/Akash Srivastava/Documents/GitHub/Buddyup/project_V1/core/x_result.pkl", "rb" ) )
            classifier_new = pickle.load(open("C:/Users/Akash Srivastava/Documents/GitHub/Buddyup/project_V1/core/classifier.pkl", "rb" ) )
            B_ok=vectorizer_new.transform(df).toarray()
            #predict label for unseen data
            df=classifier_new.predict(B_ok)
            val=len(tmp1)+1
            for j in range(0,len(tmp1)):
                if j not in ind:
                    tweet=tweets_data(twitter_handle=t_handle,tweet_id=tmp1[j],tweet_data=tmp3[j],tweet_date=tmp2[j],class_label=df[j])
                    tweet.save()


            tmp4.append([tmp,tmp1,tmp2,tmp3,df,len(tmp1)])
            '''
            df=Preprocess.preprocess1(tmp3)
            for pos,item in df.iterrows():
                tweet=tweets_data(twitter_handle=t_handle,tweet_id=tmp1[pos],tweet_data=item['Tweet'],tweet_date=tmp2[pos],sum_score=item['Sum_score'],score=item['Score'],counter=item['Counter'])
                tweet.save()


            # for final product


@task(name="Adding_friend_tweets")
def AddFriendTweets(friend_handle):


    auth=tweepy.OAuthHandler('twVFhyS2oNaSjcUUVaYVnTBpH' ,'GlvJcYHsfeT6szx7oLuVBiWgtwAg2SCEEzhJpyUuWslooI61cn')
    auth.set_access_token('1133388205372432386-zKJMvfgPa1hI5zGQgsWH7LOKBdk0wU','KYAQDWhALWNQcCF2URWtgoXNzjZkRiBueIlBGj26nQcld')
    api=tweepy.API(auth)
    public_tweets=api.user_timeline(friend_handle,count=1000,tweet_mode='extended')
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
        tmp3.append(j.full_text)
        #tweet=tweets_data(twitter_handle=friend_handle,tweet_id=j.id,tweet_data=j.text,tweet_date=j.created_at)
        #tweet.save()
        #print(tmp)
    
    # used for mvp
    '''
    df,ind=Preprocess.preprocess(tmp3)
    #input text
    #st=["I'm not unhappy today", "I love my country"]
    #transform our input text for prediction
    #unpickle the tfidf vectorizer
    vectorizer_new = pickle.load(open("C:/Users/Akash Srivastava/Documents/GitHub/Buddyup/project_V1/core/x_result.pkl", "rb" ) )
    classifier_new = pickle.load(open("C:/Users/Akash Srivastava/Documents/GitHub/Buddyup/project_V1/core/classifier.pkl", "rb" ) )
    B_ok=vectorizer_new.transform(df).toarray()
    #predict label for unseen data
    df=classifier_new.predict(B_ok)
    val=len(tmp1)+1
    for j in range(0,len(tmp1)):
        if j not in ind:
            tweet=tweets_data(twitter_handle=friend_handle,tweet_id=tmp1[j],tweet_data=tmp3[j],tweet_date=tmp2[j],class_label=df[j])
            tweet.save()


    tmp4.append([tmp,tmp1,tmp2,tmp3,df,len(tmp1)])
    '''

    # for final product
    df=Preprocess.preprocess1(tmp3)
    for pos,item in df.iterrows():
        tweet=tweets_data(twitter_handle=friend_handle,tweet_id=tmp1[pos],tweet_data=item['Tweet'],tweet_date=tmp2[pos],sum_score=item['Sum_score'],score=item['Score'],counter=item['Counter'])
        tweet.save()



    return tmp4

