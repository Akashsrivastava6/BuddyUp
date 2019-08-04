from login.models import User_detail,Registration
from core.models import following,notification_data
from passlib.hash import pbkdf2_sha256

def getFriends(usr):
    data3=following.objects.filter(user_id=usr).filter(isActive=1)
    t_handle=[]
    for d in data3:
        t_handle.append(d.twitter_handle)
    return t_handle

def checkUserPassword(usr,pwd):
    if usr=="":
        return "fail","Please enter Username"
    if pwd=="":
        return "fail","Please enter Password"
    try:
        data=User_detail.objects.get(username=usr)
    except:
        return "fail","Username not registered!"
    if pbkdf2_sha256.verify(pwd,data.password):
        return "success","ok"
    else:
        return "fail","Incorrect Password!"

def registerNewUser(usr,pwd,fname,lname,dob):
    pwd=pbkdf2_sha256.encrypt(pwd,rounds=10000)
    try:
        data=User_detail.objects.get(username=usr)
    except:
        
        user_login_details=User_detail(username=usr,password=pwd,email=usr)
        
        user_registration_details=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob)
        user_login_details.save()
        user_registration_details.save()
        
        return "You have been registered!!"
    return "Email already registered"    

def notificationdata(usr):
    data3=following.objects.filter(user_id=usr).filter(isActive=1)
    noti_list=[]
    dd1 = []
    for d in data3:
        dd = []
        # t_handle.append(d.twitter_handle)
        noti_data= notification_data.objects.filter(twitter_handle=d.twitter_handle) 
        for row in noti_data:
            noti_list.append({"handle":d.twitter_handle,"tweet":row.tweet_data})
            dd.append({"tweet":row.tweet_data,"date":row.noti_date})            
        dd1.append({"handle": d.twitter_handle, "tweet_arr": dd})

    return noti_list, dd1


def getFirstName(usr):
    fname=Registration.objects.filter(username=usr)
    return fname[0].FirstName