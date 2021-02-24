from django.shortcuts import render, redirect
from .models import User, Request, Bank
from django.conf import settings

uname=''
adminuname=''
message=''

def index(request):
    global uname
    global message
    uname=''
    return render(request,'Index.html',{'message':message})

def register(request):
    return render(request,'Register.html')

def registerUser(request):
    global uname
    name = request.POST['name']
    dob = request.POST['dob']
    email = request.POST['email']
    mobile = request.POST['mobile']
    username = request.POST['username']
    password = request.POST['password']
    bldgrp = request.POST['bldgrp']
    profile = request.FILES['profile']
    address = request.POST['address']
    uname = username
    user = User(name=name,dob=dob,email=email,mobile=mobile,username=username,password=password,bldgrp=bldgrp,profile=profile,address=address)
    user.save()
    return redirect('/Home')

def home(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        data = User.objects.all().filter(username=uname)
        return render(request,'Home.html',{'uname':uname,'data':data})

def login(request):
    a=1
    global uname
    global message
    uname = request.POST['username']
    passw = request.POST['password']
    data = User.objects.all().filter(username=uname)
    for i in data:
        if i.password == passw:
            a=0;
            message = ''
            return redirect('/Home')

    if a == 1:
        message = 'Invalid Login Credentials'
        return redirect('/')

def logout(request):
    global uname
    uname=''
    return redirect('/')

def updateprofile(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        pic = request.FILES['profile']
        t = User.objects.get(username=uname)
        t.profile = pic
        t.save()
        return redirect('/Home')

def resetpassword(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        password = request.POST['password']
        t = User.objects.get(username=uname)
        t.password = password
        t.save()
        return redirect('/Logout')

def editcontact(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        t = User.objects.get(username=uname)
        email = request.POST['email']
        mobile = request.POST['mobile']
        t.email = email
        t.mobile = mobile
        t.save()
        return redirect('/Home')

def editaddress(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        t = User.objects.get(username=uname)
        address = request.POST['address']
        t.address = address
        t.save()
        return redirect('/Home')

def searchperson(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        bldgrp = request.POST['bldgrp']
        data = User.objects.all().filter(bldgrp=bldgrp).exclude(username=uname)
        return render(request,'SearchedPerson.html',{'uname':uname,'data':data,'bldgrp':bldgrp})

def processrequest(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        username = request.POST['username']
        quantity = request.POST['quantity']
        bldgrp = request.POST['bldgrp']
        request = Request(sender=uname,reciever=username,bldgrp=bldgrp,quantity=quantity,status='pending')
        request.save()
        return redirect('/Home')

def requestsent(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        data1 = Request.objects.all().filter(sender=uname).exclude(reciever='bank').order_by('-id')
        data2 = Request.objects.all().filter(sender=uname, reciever='bank').order_by('-id')
        return render(request,'RequestSent.html',{'data1':data1,'data2':data2,'uname':uname})

def viewuser(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        username = request.POST['username']
        data = User.objects.all().filter(username=username)
        return render(request,'ViewUser.html',{'data':data,'uname':uname})

def requestrecieved(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        data1 = Request.objects.all().filter(reciever=uname, status='pending').order_by('-id')
        data2 = Request.objects.all().filter(reciever=uname).exclude(status='pending').order_by('-id')
        return render(request,'RequestRecieved.html',{'data1':data1,'data2':data2,'uname':uname})

def acceptrequest(request):
    if uname=='':
        return redirect('/')
    else:
        requestid = request.POST['id']
        t = Request.objects.get(id=requestid)
        t.status = 'accepted'
        t.save()
        return redirect('/RequestRecieved')

def rejectrequest(request):
    if uname=='':
        return redirect('/')
    else:
        requestid = request.POST['id']
        t = Request.objects.get(id=requestid)
        t.status = 'rejected'
        t.save()
        return redirect('/RequestRecieved')

def adminlogin(request):
    global adminuname
    adminuname = ''
    return render(request,'AdminLogin.html')

def checklogin(request):
    global adminuname
    credentials = {'username':'Pavanjain1996','password':'action12@on'}
    username = request.POST['username']
    password = request.POST['password']
    if username==credentials['username'] and password==credentials['password']:
        adminuname = username
        return redirect('/AdminHome')
    else:
        return redirect('/AdminLogin')

def adminhome(request):
    global adminuname
    if adminuname=='':
        return redirect('/AdminLogin')
    else:
        data = Bank.objects.all()
        return render(request,'AdminHome.html',{'adminuname':adminuname,'data':data,'bankname':'City Blood Bank','mobile':'8349312393','email':'013pavanjain@gmail.com'})

def adminlogout(request):
    global adminuname
    adminuname = ''
    return redirect('/AdminLogin')

def bloodbank(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        data = Bank.objects.all()
        return render(request,'BloodBank.html',{'uname':uname,'data':data,'bankname':'City Blood Bank','mobile':'8349312393','email':'013pavanjain@gmail.com'})

def processbankrequest(request):
    global uname
    if uname=='':
        return redirect('/')
    else:
        bldgrp = request.POST['bldgrp']
        quantity = request.POST['quantity']
        request = Request(sender=uname,reciever='bank',bldgrp=bldgrp,quantity=quantity,status='pending')
        request.save()
        return redirect('/Home')

def bankrequest(request):
    global adminuname
    if adminuname=='':
        return redirect('/AdminLogin')
    else:
        data = Request.objects.all().filter(reciever='bank', status='pending').order_by('-id')
        data1 = Request.objects.all().filter(reciever='bank').exclude(status='pending').order_by('-id')
        return render(request,'BankRequest.html',{'adminuname':adminuname,'data':data,'data1':data1})

def acceptbankrequest(request):
    requestid = request.POST['id']
    t = Request.objects.get(id=requestid)
    t.status = 'accepted'
    t.save()
    return redirect('/AdminHome')

def rejectbankrequest(request):
    requestid = request.POST['id']
    t = Request.objects.get(id=requestid)
    t.status = 'rejected'
    t.save()
    return redirect('/AdminHome')

def viewadminuser(request):
    global adminuname
    username = request.POST['username']
    data = User.objects.all().filter(username=username)
    return render(request,'ViewAdminUser.html',{'data':data,'adminuname':adminuname})

def alterstock(request):
    bldgrp = request.POST['bldgrp']
    status = request.POST['status']
    t = Bank.objects.get(bldgrp=bldgrp)
    t.status = status
    t.save()
    return redirect('/AdminHome')

def forgotpassword(request):
    global message
    return render(request,'ForgotPassword.html',{'message':message})

def changepassword(request):
    global message
    username = request.POST['username']
    password = request.POST['password']
    try:
        t = User.objects.get(username=username)
        t.password = password
        t.save()
        message = ''
        return redirect('/')
    except:
        message = 'User does not exist'
        return redirect('/ForgotPassword')
