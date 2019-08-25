from django.db.models import Count,Max
from celery.decorators import task,periodic_task
from celery.task.schedules import crontab
from django.core.mail import send_mail
from core.models import following,tweets_data,notification_data
from login.models import User_detail,Registration
import login.task
import json
import datetime
from datetime import date, datetime,timezone,timedelta
import tweepy
from . import Preprocess
import pickle
import pandas as pd
import spacy

# method to send request to friend to join buddyUp
def sendRequest(usr,friend_handle,friend_email,url):
    
    data=following.objects.filter(user_id=usr).filter(twitter_handle=friend_handle) # checking if the user has added the friend before
    if len(data)>0: # if the friend data is already id db then following page is returned
        t_handle,t_handle2=login.task.getFriends(usr) # geting data to update followers list
        return t_handle,t_handle2,"Request already sent for this twitter handle." #
    else: # if the friend is added for the first time.
        friend_tweet=following(user_id=usr,twitter_handle=friend_handle,friend_Email=friend_email,url=url) # adding friends details in db
        friend_name=login.task.getFirstName(usr) # retrieving frist name of the logged in user
        send_mail("Request From " + friend_name + " to join BuddyUp.", "Hi,\n\nYour friend " + friend_name + ", wants to add you on BuddyUp. BuddyUp is a web Application which generates and shows trend based on the recent twitter activity. Please read the below privacy policy and take the action.\n\nPrivacy Notice: This notice is to inform you that as a part of a research project BUDDYUP undertaken for the completion of masters’ degree Computer Science Negotiated Learning at University College Dublin. The research group shall be analyzing your twitter handle which comprises of Twitter Username and Password to understand human behavior. To details on the processing of personal data, we wish to inform you that your personal data shall be stored in the database for profile creation and granting access to your tweets to " +  friend_name  +
                  ". Please be informed that the information obtained under this research project will be erased without the possibility of reverse engineer, within 3 months from the submission of the research project. The motive of this research is to provide a tool that continuously monitors and notifies the emotional well being of loved ones on Twitter. Please note that the data obtained from this research project is purely for academic and non-commercial purpose. As we respect your right to privacy and in compliance with GDPR and ePrivacy Directives, we wish to procure a freely given, informed, unambiguous and explicit consent for processing the personal data available in your twitter handle. \n\nBy clicking on the link, you can provide your consent and register with us. However, you do have an option to opt out of this research project by ignoring this mail. If you need any further details on the research project, you may feel free to contact us on support@buddyup.cc. We would be happy to walk you through the research outcomes.\n\n buddyup.cc/oauth/login/twitter/ \n\n Thanks,\n BuddyUp Team", "a.team.ucd.5@gmail.com", [friend_email])  # sending mail to the friend
        friend_tweet.save()
        t_handle,t_handle2=login.task.getFriends(usr) # geting data to update followers list
        return t_handle,t_handle2,"An Email is sent for Confirmation!" # returning the page and data
        


# method to send the data as json to temolate
def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)): 
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

# method to retrun the list of followers
def getFollower(user):
    data3=following.objects.filter(twitter_handle=user) # retreivig all the follower for the twitter handle
    followed=[]
    for d in data3:
        user=""
        user=d.user_id
        if d.isActive==0: # checking if the isActive is 0
           followed.append({"user":user,"status":"Grant Access"}) #if isActive is 0 then status is Grant Access
        else:
            followed.append({"user":user,"status":"Revoke Access"}) # if isActive is not 0 then status is revoke access
    return followed # return followers list

#method to return data for trend page
def getTrend(twitter_handle):
    now=datetime.now()-timedelta(days=10) # setting variable with value as date 10 days back

    tweet_data=tweets_data.objects.filter(twitter_handle=twitter_handle).filter(tweet_date__gt=now) # retreiving tweets for a twitter handle tweeted within last 10 days
            
    tweet_dat=[]
    scores=[]
    for a in tweet_data: # iterating the tweet_data returned from the db
        tweet_dat.append({"id":a.tweet_id,"tweet_data":a.tweet_data,"tweet_date":a.tweet_date,"tweet_score":a.score,"tweet_sum_score":a.sum_score,"tweet_counter":a.counter,"is_noti":a.is_notification}) # appending the tweet data to a list
        scores.append([a.tweet_date,a.score]) # appending tweet score to a list
    score1=pd.DataFrame(scores,columns=['date','score']) #creating dataframe of date and score of tweet

    # following code is used to compute moving average
    cumsum, moving_aves = [0], []
    if len(score1)>0:
        dd=score1.set_index('date').groupby(pd.Grouper(freq='D')).mean() # average score of each day is calculated
        dd=dd.dropna() # None values are dropped from dataframe
        mylist = dd['score'].tolist() #dataframe is converted to list
        if len(mylist) >10: #setting the value of N
            N=10
        else:
            N=len(mylist)


        

        #movinf average is calculated
        for i, x in enumerate(mylist, 1): 
            cumsum.append(cumsum[i-1] + x)
            if i>=N:
                moving_ave = (cumsum[i] - cumsum[i-N])/N
                
                moving_aves.append(moving_ave)
    
    if len(moving_aves)>0:   # if there is a row in list then
        summ=moving_aves[-1]# the last values from the list is taken
    else:
        summ=101 #101 is returned in case list is empty
    
    return json.dumps(tweet_dat, default=json_serial),tweet_dat,twitter_handle,json.dumps(tweet_dat,default=json_serial),json.dumps(tweet_dat,default=json_serial),summ # data iis returned

# this metod is executed when user logs in through twitter
def twitterCheck(username):
    d1=User_detail.objects.filter(username=username) # user detail is retieved from the database
    if len(d1)>0: # checking if the user exists 
        #following coed is executed if the usename exist
        d2=Registration.objects.filter(username_id=username) # checking if the username has data in registration table 
        if len(d2)>0:    #checking if the user deatils exists in the registration table as well then
            userfollowing=following.objects.filter(twitter_handle=username) # data from following table is retrieved for the twitter handle
            if len(userfollowing)>0: #checking if there are follower of the user  
                if len(userfollowing.filter(isActive=1))>0: #checking if the user has given acces to any of the followers 
                    t_handle,t_handle2=login.task.getFriends(username) # retreiving list of friends the user is following
                    return 'dashboard.html',t_handle,t_handle2,180 # returning dashboard and the list and session timeout value
                else: # if the user has not given access to any of the follower
                    t_handle=getFollower(username) # retreiving the list of followers
                    return 'followers.html',t_handle,None,180 # followers page is returned along with the list of followers and session timeout value
            else: # if the use is not followed by any other user
                t_handle,t_handle2=login.task.getFriends(username) # retreiving the list of friends the user follows
                return 'dashboard.html',t_handle,t_handle2,180 # returning the list of friends and the session timeout value
        else: # if the user doesnt have data in registration table
            return 'editprofile.html',None,None,10      
    else:  # if the user logs in for the first time              
        adduserD=User_detail(username=username.lower()) # user details are added ti user)detail table
        # adduserR=Registration(username_id=extra,firstname=userdata.first_name,lastname=userdata.last_name)
        
        adduserD.save() # the details are commited
        return 'editprofile.html',None,None,10 #edit page is returned along with session timeout value
        
                
# the following method is used to send the notification whenever there is a notifiable twwet
@periodic_task(run_every=(crontab(minute='*/1')), name="noti_task", ignore_result=True)
def noti_task():
    
    t_handles=following.objects.filter(isActive=1)  # reteiving the list twitter handle who has given acces to atleat one user


    for a in t_handles: # iterating through t_handles
        data=notification_data.objects.filter(is_notified=0).filter(twitter_handle=a.twitter_handle) # retreiving the list tweets from the table that are not notified yet

        for ad in data: # iterating through data

            friendlist=[]
            print(data)
            print(ad)
            frienddata=following.objects.filter(twitter_handle=ad.twitter_handle).filter(isActive=1) # retreiving the lsit of user to who the particular twitter handle has given access

            for ab in frienddata: # for each user 
                email=User_detail.objects.filter(username=ab.user_id) # email id of each user is retrieved 
                for abc in email:
                    print(abc)
                    friendlist.append(abc.email) # email is added to a list
                    print(ad.id)
                    friend_name=login.task.getFirstName(ab.user_id) #first name friend is retrieved
                    send_mail("Tweet Alert","Hi "+friend_name+',\n\nThis mail is regarding your friend with twitter handle : '+ad.twitter_handle+'. @'+ad.twitter_handle+' has tweeted something which may be of concern to you.\n\n            Tweet : "'+ad.tweet_data+'"\n\nPlease talk to your friend to check on his well being.\n\n Thanks,\nTeam BuddyUp',"a.team.ucd.5@gmail.com",[abc.email]) # notification email is send
                    d=notification_data.objects.filter(id=ad.id).update(is_notified=1) # the particular tweets row is updated in the database as notified.


# the following task is executed to retrieve tweets in fixed interval of time
@periodic_task(run_every=(crontab(minute='*/1')), name="AddTweets_task", ignore_result=True)
def AddTweets():
    data=following.objects.filter(isActive=1) # lsit of twitter handle who has given access to any of the user is retreived
    dep_list=pd.read_csv("core\\dep_list.csv") # list of depression words is retrieved 
    for d in data: # for each row in data
        t_handle=d.twitter_handle # twitter handle is retrieved
        maxid=tweets_data.objects.filter(twitter_handle=t_handle).aggregate(Max('tweet_id'))    # most recent tweet is retrieved for a twitter handle
        auth=tweepy.OAuthHandler('twVFhyS2oNaSjcUUVaYVnTBpH' ,'GlvJcYHsfeT6szx7oLuVBiWgtwAg2SCEEzhJpyUuWslooI61cn') # oAuth toekns
        auth.set_access_token('1133388205372432386-zKJMvfgPa1hI5zGQgsWH7LOKBdk0wU','KYAQDWhALWNQcCF2URWtgoXNzjZkRiBueIlBGj26nQcld') # secret
        api=tweepy.API(auth) #
        public_tweets=api.user_timeline(t_handle,since_id=str(maxid['tweet_id__max']),count=1000,tweet_mode='extended') # tweets are retrieved with the id grater than the last tweet id of a particular twitter handle
        #print(public_tweets.name)
        tmp=[]
        tmp1=[]
        tmp2=[]
        tmp3=[]
        tmp4=[]
        #tweets_for_csv=for tweet in public_tweets

        
        for j in public_tweets: # for each row in public_tweets

            tmp1.append(j.id)
            tmp2.append(j.created_at)
            tmp3.append(j.full_text)
            
        if len(tmp3)>0: # checking of there are tweets
            # for mvp
            sp=spacy.load('en_core_web_sm')    # loading the spacy english package       
            df=Preprocess.preprocess1(tmp3) # calling the method to preprocess the tweets and get score for each tweet
             # added on 31 july to check. this needs to be tested.
            for pos,item in df.iterrows(): # iterating through the datafarme
                tweet=tweets_data(twitter_handle=t_handle,tweet_id=tmp1[pos],tweet_data=item['Tweet'],tweet_date=tmp2[pos],sum_score=item['Sum_score'],score=item['Score'],counter=item['Counter']) # saving the tweet data tp db
                tweet.save() # commitng the changes in db
                
                if item['Score']<-1: # checking if the score of tweets is less than -1
                    pronounlistf=['i','me','mine','we','us','our','ours','my','myself'] # lsit of self reflecting personal pronoun
                    pronounlisto=['your','yours','he','him','his','she','her','hers','they','them','their','theirs' ] # list of non self reflecting personal pronoun
                    d_flag=0 #setting flag as 0
            #print11(sen.text)

                    listl=[]
                    listll=[]
                    text = item['Tweet'] # retrieving tweets text
                    c1=0
                    c2=0
                    d_flag=0       
                    sen=sp(text) 
                    
                    for word in sen: # for each word in sen
                        if (word.tag_ =='PRP') or (word.tag_ =='PRP$'): # checking if the word is a personal pronoun
                            if word.text.lower() in pronounlistf: # checking if the the word is self reflecting personal pronoun
                        #                 listl.append(word.text)
                                        #print(text+":"+word.text+"c1")
                                
                                c1=c1+1 # incremating the counter
                            elif word.text.lower() in pronounlisto: #checking if the word is not self reflecting personal pronoun
                                        #print(text+":"+word.text+"c2")
                                c2=c2+1 # incrementin the counter
                                
                            if c1 == 0 and c2==0: # checking if the two counters are equal
                                d_flag=1 # setting the flag as 1
                            elif c1>c2: # if self reflecting personal pronoun are more than non self reflecting personal pronoun
                                d_flag=2
                                
                            else:        
                                pass
                            if d_flag==1:    # checing if the flag is 1 that is there are self reflecting personal pronoun in the tweet
                                for word in sen:
                                    if word.text.lower() in dep_list['WORD'].values: # if the word is in dep list
                                        d_flag=2
                                        
                       
                    if d_flag==2: # checking if the twwet is notifiable or not if d_flag is 2 then it is notifiable
                        # print(t_handle+"  "+text+" "+str(date.today))
                        d=tweets_data.objects.filter(twitter_handle=t_handle).filter(tweet_id=tmp1[pos]).update(is_notification=1) # updating the tweet as notifiable
                        not_data=notification_data(twitter_handle=t_handle,tweet_data=text,noti_date=datetime.now(timezone.utc),is_notified=0) # adding data to notification _data table
                        not_data.save() 
                    
               

# the following method is called when the user grants access to a friend for the first time
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

