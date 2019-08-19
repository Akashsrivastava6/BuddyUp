from login.models import User_detail,Registration
from core.models import following,notification_data
from passlib.hash import pbkdf2_sha256
from datetime import date


# the following method return the list of friends for a particular user
def getFriends(usr):
    data3=following.objects.filter(user_id=usr).filter(isActive=1) # retreiving the lst of friends who has given access to the user
    data34=following.objects.filter(user_id=usr).filter(isActive=0) # retreiving the list of friend who have not given acess to the user
    t_handle=[]
    t_handle2=[]
    for d in data3:
        t_handle.append(d.twitter_handle) # adding the friend who have given access into a list
    for dd in data34:
        t_handle2.append(dd.twitter_handle)# adding the friend who have not given access into a list
    return t_handle,t_handle2 # returning the list of friends


# method to check the password for a username
def checkUserPassword(usr,pwd):
    if usr=="": # checking if the username is emoty
        return "fail","Please enter Username" 
    if pwd=="": # checking the upassword is emoty
        return "fail","Please enter Password"
    try: # checking if the username is registered
        data=User_detail.objects.get(username=usr)
    except:
        return "fail","Username not registered!"
    if pbkdf2_sha256.verify(pwd,data.password): # checking if the users password
        return "success","ok" # if password for a user is matched
    else:
        return "fail","Incorrect Password!"
# method to register new user
def registerNewUser(usr,pwd,fname,lname,dob):
    pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000) #encrypting the user password
    try:
        data=User_detail.objects.get(username=usr) # chekcing tif the user is alreadu=y registered
    except:
        # if the user is not registered
        user_login_details=User_detail(username=usr,password=pwd,email=usr) # registering the user
        
        user_registration_details=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob)
        user_login_details.save()
        user_registration_details.save()
        
        return usr
    return "Email already registered"    

# method to retrieve notification data
def notificationdata(usr):
    data3=following.objects.filter(user_id=usr).filter(isActive=1) #Retrieving the list of friend who have given access to a particular user
    noti_list=[]
    dd1 = []
    
    for d in data3:
        dd = []
        # t_handle.append(d.twitter_handle)
        noti_data= notification_data.objects.filter(twitter_handle=d.twitter_handle)  # retreiving the notifiable tweets for a friend
        for row in noti_data:
            noti_list.append({"handle":d.twitter_handle,"tweet":row.tweet_data})    # adding the tweets to a list
            dd.append({"tweet":row.tweet_data,"date":row.noti_date.date(),"datetime":row.noti_date})  # adding the tweets and date to a list
        dd=dd[::-1] # reversing the list
        dd1.append({"handle": d.twitter_handle, "tweet_arr": dd})
        
    return noti_list, dd1

# method to return firstname for a username
def getFirstName(usr):
    fname=Registration.objects.filter(username=usr)
    return fname[0].FirstName
# method to return last login time of a user
def getLastLogin(usr):
    last_login=User_detail.objects.filter(username=usr)
    return last_login[0].last_login

