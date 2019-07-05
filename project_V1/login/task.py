from login.models import User_detail,Registration
from core.models import following
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
        
        user_login_details=User_detail(username=usr,password=pwd)
        
        user_registration_details=Registration(username_id=usr,FirstName=fname,LastName=lname,dateOfBirth=dob)
        user_login_details.save()
        user_registration_details.save()
        
        return "You have been registered!!"
    return "Email already registered"    
