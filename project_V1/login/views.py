from django.shortcuts import render,redirect
from login.models import User_detail,Registration
from django.contrib.auth.decorators import login_required
from core.models import following
from login import task 

@login_required
def home(request):
    return render(request, 'index.html')

# Create your views here.
def loginPage(request):

    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        t_handle=task.getFriends(usr)
        return render(request,'dashboard.html',{'Message':request.session['username'],'data':t_handle})
    return render(request,'index.html')

def logoutRequest(request):
    try:
        del request.session['username']
        request.session.set_expiry(1)
    except KeyError:
        pass
   # return render(request,'index.html',{"Message":"Logout Successful!"})
    return redirect("/login")


def signupUser(request):
    return render(request,'signup.html')

def myprofile(request):
    return render(request,'myprofile.html')

def about(request):
    return render(request, 'about.html')

def loginRequest(request):

    if request.session.has_key('username'):
        request.session.set_expiry(180)
        usr=request.session['username']
        t_handle=task.getFriends(usr)
        noti_list, dd1=task.notificationdata(usr)
        return render(request,'dashboard.html',{'Message':request.session['username'],'data':t_handle,'noti':noti_list,'dd1':dd1})
    request.session.clear_expired()
    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    status,message=task.checkUserPassword(usr,pwd)
    if status=="fail":
        return render(request,'index.html',{'Message':message})
    elif status=="success":
        request.session.set_expiry(180)
        request.session['username']=usr
        t_handle=task.getFriends(usr)
        noti_list,dd1=task.notificationdata(usr)
        return render(request, 'dashboard.html', {'Message': request.session['username'], 'data': t_handle, 'noti': noti_list, 'dd1': dd1})
        

def RegisterUser(request):
    
    usr=request.POST.get("username")
    pwd=request.POST.get('password')
    fname=request.POST.get("fname")
    lname=request.POST.get("lname")
    dob=request.POST.get("dob")
    message=task.registerNewUser(usr,pwd,fname,lname,dob)
    return render(request,'signup.html',{'Message':message})
    

    
