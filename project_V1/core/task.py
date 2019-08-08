from django.db.models import Count,Max
from celery.decorators import task,periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from core.models import following,tweets_data,notification_data
from login.models import User_detail,Registration
import login.task
import json
import datetime
from datetime import date, datetime,timezone
import tweepy
from . import Preprocess
import pickle
import pandas as pd
import spacy


def sendRequest(usr,friend_handle,friend_email,url):
    t_handle=login.task.getFriends(usr) 
    data=following.objects.filter(user_id=usr).filter(twitter_handle=friend_handle)
    if len(data)>0:
        
        return t_handle,"Request already send for this twitter handle."
    else:
        friend_tweet=following(user_id=usr,twitter_handle=friend_handle,friend_Email=friend_email,url=url)
        friend_name=login.task.getFirstName(usr)
        send_mail("Request From "+ friend_name+ " to join BuddyUp.","Hi,\n\nYour friend "+ friend_name +", wants to add you on BuddyUp. BuddyUp is a webapp which generates and shows trend based on the recent twitter activity. Please read the below privacy policy and take the action.\n\nPrivacy Notice: This notice is to inform you that as a part of a research project [name of the project] undertaken for the completion of masters’ degree Computer Science Negotiated Learning at University College Dublin. The research group shall be analyzing your twitter handle which comprises of [type of data] to understand human behavior. This information is anonymously used for the research project and does not directly or specifically identify you. To details on the processing of personal data, we wish to inform you that your personal data shall be [Process]. Please be informed that the information obtained under this research project will be erased without the possibility of reverse engineer, within 3 months from the submission of the research project. The motive of this research [elaborate on the outcome of the research]. Please note that the data obtained from this research project is purely for academic and non-commercial purpose. As we respect your right to privacy and in compliance with GDPR and ePrivacy Directives, we wish to procure a freely given, informed, unambiguous and explicit consent for processing the personal data available in your twitter handle. \n\nBy click on the link, you can provide your consent and register with us. However, you do have an option to opt out of this research project by ignoring this mail. If you need any further details on the research project, you may feel free to contact us on mail@ucd.ie. We would be happy to walk you through the research outcomes.\n\n 127.0.0.1:8000/oauth/login/twitter/ \n\n Thanks,\n BuddyUp Team","a.team.ucd.5@gmail.com",[friend_email])
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
    tweet_dat=[]
    for a in tweet_data:
        tweet_dat.append({"id":a.tweet_id,"tweet_data":a.tweet_data,"tweet_date":a.tweet_date,"tweet_score":a.score,"tweet_sum_score":a.sum_score,"tweet_counter":a.counter,"is_noti":a.is_notification})





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
        df.to_csv("core/testlist1.csv", encoding='utf-8-sig')
    '''
    return json.dumps(tweet_dat, default=json_serial),tweet_dat,twitter_handle,json.dumps(tweet_dat,default=json_serial),json.dumps(tweet_dat,default=json_serial)


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
        adduserD=User_detail(username=username.lower())
        # adduserR=Registration(username_id=extra,firstname=userdata.first_name,lastname=userdata.last_name)
        
        adduserD.save()
        return 'editprofile.html',None
        #adduserR.save()
        # userfollowing=following.objects.filter(twitter_handle=username)
        # if len(userfollowing)>0:
        #     if len(userfollowing.filter(isActive=1))>0:             
        #         t_handle=login.task.getFriends(username)
        #         return 'dashboard.html''data',t_handle
        #     else:
        #         t_handle=getFollower(username)
        #         return 'followers.html',t_handle
        # else:
        #     t_handle=login.task.getFriends(username)
        #     return 'dashboard.html',t_handle
                

@periodic_task(run_every=(crontab(minute='*/1')), name="noti_task", ignore_result=True)
def noti_task():
    # t_handles=following.objects.filter(isActive=1)
    
    # for a in t_handles:
    #     twts=notification_data.objects.filter(twitter_handle=a.twitter_handle)
        
    #     friendlist=[]
    #     frienddata=following.objects.filter(twitter_handle=a.twitter_handle)
        
        
    #     for ab in frienddata:
    #         friendlist.append(ab.user_id)        
    #     if len(twts)>0:
    #        # print("length is 1"+friendlist[0])
    #         cur_date=datetime.now(timezone.utc)
    #         max_date=notification_data.objects.filter(twitter_handle=a.twitter_handle).values('noti_date').annotate(mx_date=Max('noti_date'))
    #         for abc in max_date:
    #             #print(abc)
    #             #print(abc['mx_date'])
    #             #print("printing mx_date : "+mx_date)
    #             dt=cur_date-abc['mx_date']
    #             #print(abc)
    #             if ((dt.seconds/(60))<1):
    #                 for email in friendlist:
    #                     print(email)
    #                     send_mail("test mail","127.0.0.1:8000/oauth/login/twitter/ %s"%a.twitter_handle,"a.team.ucd.5@gmail.com",[email])

    
    t_handles=following.objects.filter(isActive=1)


    for a in t_handles:
        data=notification_data.objects.filter(is_notified=0).filter(twitter_handle=a.twitter_handle)

        for ad in data:

            friendlist=[]
            print(data)
            print(ad)
            frienddata=following.objects.filter(twitter_handle=ad.twitter_handle).filter(isActive=1)

            for ab in frienddata:
                email=User_detail.objects.filter(username=ab.user_id)
                for abc in email:
                    print(abc)
                    friendlist.append(abc.email)
                    print(ad.id)
                    friend_name=login.task.getFirstName(ab.user_id)
                    send_mail("test mail","Hi "+friend_name+',\n\nHope you are doing good. This mail is regarding your friend with twitter handle : '+ad.twitter_handle+'. @'+ad.twitter_handle+' has tweeted something which may be of concern to you.\n\n            Tweet : "'+ad.tweet_data+'"\n\nPlease talk to your friend to check on his well being.\n\n Thanks,\nTeam BuddyUp',"a.team.ucd.5@gmail.com",[abc.email])
                    d=notification_data.objects.filter(id=ad.id).update(is_notified=1)



        # if len(twts)>1:
        #     print("no notification")

        # elif len(twts)==1:


        #     send_mail("test mail","127.0.0.1:8000/oauth/login/twitter/","a.team.ucd.5@gmail.com",[friend_email])
        # else:
        #     print("No tweet")




@periodic_task(run_every=(crontab(minute='*/2')), name="AddTweets_task", ignore_result=True)
def AddTweets():
    data=following.objects.filter(isActive=1)
    dep_list=pd.read_csv("core\\dep_list.csv")
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
            sp=spacy.load('en_core_web_sm')           
            df=Preprocess.preprocess1(tmp3)
             # added on 31 july to check. this needs to be tested.
            for pos,item in df.iterrows():
                tweet=tweets_data(twitter_handle=t_handle,tweet_id=tmp1[pos],tweet_data=item['Tweet'],tweet_date=tmp2[pos],sum_score=item['Sum_score'],score=item['Score'],counter=item['Counter'])
                tweet.save()
                

            
            # da_for_use=df[df['Score']<-1]
            # da_for_use

        ##tokens=nltk.word_tokenize(da_for_use.iloc[5]['Tweet'])
        #tags=nltk.pos_tag(tokens)
                if item['Score']<-1:
                    pronounlistf=['i','me','mine','we','us','our','ours','my','myself']
                    pronounlisto=['your','yours','he','him','his','she','her','hers','they','them','their','theirs' ]
                    d_flag=0
            #print11(sen.text)

                    listl=[]
                    listll=[]
                    text = item['Tweet']
                    c1=0
                    c2=0
                    d_flag=0       
                    sen=sp(text)
                    for word in sen:
                        if (word.tag_ =='PRP') or (word.tag_ =='PRP$'):
                            if word.text.lower() in pronounlistf:
                        #                 listl.append(word.text)
                                        #print(text+":"+word.text+"c1")
                                c1=c1+1
                            elif word.text.lower() in pronounlisto:
                                        #print(text+":"+word.text+"c2")
                                c2=c2+1
                            if c1 == 0 and c2==0:
                                d_flag=1
                            elif c1>c2:
                                d_flag=2
                            else:        
                                pass
                            if d_flag==1:    
                                for word in sen:
                                    if word.text.lower() in dep_list['WORD'].values:
                                        d_flag=2
                    if d_flag==2:
                        # print(t_handle+"  "+text+" "+str(date.today))
                        d=tweets_data.objects.filter(twitter_handle=t_handle).filter(tweet_id=tmp1[pos]).update(is_notification=1)
                        not_data=notification_data(twitter_handle=t_handle,tweet_data=text,noti_date=datetime.now(timezone.utc))
                        not_data.save()
                    
                #print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {word.dep_:{10}} {spacy.explain(word.tag_)}')
      

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

    sp=spacy.load('en_core_web_sm')
    da_for_use=df[df['Score']<-1]
    da_for_use

##tokens=nltk.word_tokenize(da_for_use.iloc[5]['Tweet'])
#tags=nltk.pos_tag(tokens)

    pronounlistf=['i','me','mine','we','us','our','ours']
    pronounlisto=['your','yours','he','him','his','she','her','hers','they','them','their','theirs' ]

#print11(sen.text)

    listl=[]
    listll=[]
    for text in da_for_use['Tweet']:
        c1=0
        c2=0
    
        sen=sp(text)
        for word in sen:
            if (word.tag_ =='PRP') or (word.tag_ =='PRP$'):
                if word.text.lower() in pronounlistf:
#                 listl.append(word.text)
                #print(text+":"+word.text+"c1")
                    c1=c1+1
                elif word.text.lower() in pronounlisto:
                #print(text+":"+word.text+"c2")
                    c2=c2+1
        if c1 == 0 and c2==0:
            listl.append(text)
            listll.append("alert")
        elif c1>c2:
            listl.append(text)
            listll.append("alert")
        else:        
            listl.append(text)
            listll.append("No alert")
                
        
        #print(f'{word.text:{12}} {word.pos_:{10}} {word.tag_:{8}} {word.dep_:{10}} {spacy.explain(word.tag_)}')
    dd=pd.DataFrame(listl)
    dd['is Alert?']=listll
    dd.columns=['Tweet','is Alert']

    dd.to_csv("core/alertlist.csv")
    return tmp4

