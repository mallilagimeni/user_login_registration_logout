from django.shortcuts import render

# Create your views here.
from app.models import *
from app.forms import *
#from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request,'home.html',d)
    
    return render(request,'home.html')
def registrations(request):
    UFD=UserForm()
    PFD=ProfileForm()
    d={'UFD':UFD,'PFD':PFD}
    if request.method=='POST' and request.FILES:
        UDC=UserForm(request.POST)
        PDC=ProfileForm(request.POST,request.FILES)
        if UDC.is_valid() and PDC.is_valid():
            NSUO=UDC.save(commit=False)
            NSUO.set_password(UDC.cleaned_data['password'])
            NSUO.save()

            NSFO=PDC.save(commit=False)
            NSFO.username=NSUO
            NSFO.save()
            #send_mail('registrations','successfully','lagimenimalli00@gmail.com',[NSUO.email],fail_silently=False)
            return HttpResponse('inserted data')
        else:
            return HttpResponse('invalid data')
    return render(request,'registrations.html',d)


def user_login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        AUO=authenticate(username=username,password=password)
        if AUO and AUO.is_active:
            login(request,AUO)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse('invalid username or password')
    return render(request,'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))

@login_required
def display_profile(request):
    username=request.session.get('username')
    UO=User.objects.get(username=username)
    PO=Profile.objects.get(username=UO)
    d={'UO':UO,'PO':PO}
    return render(request,'display_profile.html',d)


@login_required
def change_password(request):
    if request.method=='POST':
        pw=request.POST['pw']
        username=request.session.get('username')
        UO=User.objects.get(username=username)
        UO.set_password(pw)
        UO.save()
        return HttpResponse('password changed successfully....!')


    return render(request,'change_password.html')

def forgot_password(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        LUO=User.objects.filter(username=username)
        if LUO:
            UO=LUO[0]
            UO.set_password(password)
            UO.save()
            return HttpResponse('password updated..!!!')
        else:
            return HttpResponse('invalid Username')
    return render(request,'forgot_password.html')












