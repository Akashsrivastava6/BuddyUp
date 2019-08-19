from django.shortcuts import render,redirect
from login.models import User_detail,Registration
from django.contrib.auth.decorators import login_required
from core.models import following
import core.task
from login import task 
from datetime import datetime,timezone

@login_required
def home(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'index.html')
# Create your views here.

#
def loginPage(request):

    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        t_handle,t_handle2=task.getFriends(usr)
        fname=task.getFirstName(usr)
        noti_list, dd1 = task.notificationdata(usr)
        return render(request, 'dashboard.html', {'Message': fname, 'data': t_handle,"data2":t_handle2, 'noti': noti_list})
    return render(request,'homepage.html')


# method when user logs out
def logoutRequest(request):
    try:
        del request.session['username'] # session is deleted
        request.session.set_expiry(1)
    except KeyError:
        pass
   # return render(request,'index.html',{"Message":"Logout Successful!"})
    return redirect("/home") # redirected to home page

# method when help us get better button is clicked in trend page
def personalisation(request):
    if request.session.has_key('username'): # Checking if user is logged in
        request.session.set_expiry(180) # updating session
        usr = request.session['username']
        fname = task.getFirstName(usr)
        twitter_handle = request.GET.get('twitter_handle')
        message, tweet_data, friend, obj1, obj2,summ = core.task.getTrend(twitter_handle) #retreiving the tweets for a twitter handle
        
        return render(request, 'personalisation.html', {'Message': fname, "tweet_data": tweet_data[0:10], 'twitter_handle': twitter_handle}) # retruning the personaliztion page along with the data
    return redirect("/login") # redirecting to login page if user session is expired or user is not logged in
        
# method when sign up button is clicked        
def signupUser(request):
    return render(request,'signup.html',{"Message":"n"})


def myprofile(request):
    return render(request,'myprofile.html')

# method when help page is requested
def about(request):
    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        fname=task.getFirstName(usr)
        return render(request, 'about.html',{'Message':fname})
    return redirect("/login")


# method when user tries to log in
def loginRequest(request):

    if request.session.has_key('username'): # checking if the user is logged in
        request.session.set_expiry(180) # updating the session
        usr=request.session['username']
        t_handle,t_handle2=task.getFriends(usr) # retreiving the first name of user
        noti_list, dd1=task.notificationdata(usr) # retreiving th elist of notifiable tweets
        last_login=task.getLastLogin(usr) # retreiving the last login details
        co=0
        for a in dd1:
            for b in a["tweet_arr"]:
                if b["datetime"]>last_login: # checking if there is any new tweet after last login  
                    co=co+1
        fname=task.getFirstName(usr) # retreving the first name
        d=User_detail.objects.filter(username=usr).update(last_login=datetime.now(timezone.utc)) #updating the last login time for the user in db
        return render(request,'dashboard.html',{'Message':fname,'data':t_handle,"data2":t_handle2,'noti':noti_list,'dd1':dd1,"last_login":co})# returning the dasboard page and data
    request.session.clear_expired()
    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    status,message=task.checkUserPassword(usr,pwd) # checking the username and password
    if status=="fail":
        return render(request,'index.html',{'Message':message}) # if the status if fail 
    elif status=="success": # if the user provides correct username and password
        request.session.set_expiry(180) # updating the session
        request.session['username']=usr
        t_handle,t_handle2=task.getFriends(usr) # retreiving the friend lists
        noti_list,dd1=task.notificationdata(usr) # retreiving the list of notifiable tweets
        last_login=task.getLastLogin(usr)
        co=0
        for a in dd1:
            for b in a["tweet_arr"]:
                if b["datetime"]>last_login: # checking if there is any new tweet after last login  
                    co=co+1
        d=User_detail.objects.filter(username=usr).update(last_login=datetime.now(timezone.utc)) # updating the last login for the user in db
        fname=task.getFirstName(usr) # retreiving the frst namr 
        return render(request, 'dashboard.html', {'Message': fname, 'data': t_handle,"data2":t_handle2, 'noti': noti_list, 'dd1': dd1,"last_login":co}) # returning the dashboard page wth data
        
# method when user registers 
def RegisterUser(request):
    
    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    dob=request.POST.get("dob")
    message=task.registerNewUser(usr,pwd,fname,lname,dob)
    return render(request,'signup.html',{'Message':message})
    

    
