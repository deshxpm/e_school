import string

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.shortcuts import render,redirect,HttpResponse
from django.contrib.auth import login, authenticate, logout
from accounts.forms import RegistrationForm, AccountAuthenticationForm,NumberForm,UpdateProfileForm
from django.contrib.auth.decorators import login_required
# from .otp_service import *
# from .models import Account
# from .models import Account

import random

Account=settings.AUTH_USER_MODEL
# Django Admin
# Email: desh2@gmail.com 
# Username: desh1
# Password: 12345

# *marked for our faculty (department our faculty and other faculty)
# Add like button
# Category for courses 


def index(request):
    return render(request,'accounts/home.html')


def generate_opt():
    n=random.randrange(1000,9999)
    return n

# otp=1234



def registration_view(request):
    context = {}
    redirect_to = request.GET.get('next', '')
    if redirect_to != "" or redirect_to is not None:
        context['redirect_to'] = redirect_to
    if request.POST:

        form = RegistrationForm(request.POST)
        if form.is_valid():

            customer_number = form.cleaned_data.get('mobile')
            # print(customer_number)
            # user_otp = form.cleaned_data.get('otp')
            # print(user_otp)
            # send_otp(customer_number,user_otp)
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password1')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else: #GET request
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'accounts/register.html', context)


def registration_with_js_form(request):
    if request.method=='POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        mobile_number=request.POST.get('mobile_number')
        email=request.POST.get('email')
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        checkbox=request.POST.get('checkbox')

        print([first_name,last_name,mobile_number,email,password,confirm_password,checkbox],3789020298890)

        if checkbox==False:
            """Redirect with error message"""
            return redirect('home')


        if(password!=confirm_password):
            """Redirect with error message"""
            return redirect('home')


        code =''.join(random.choices(string.ascii_uppercase , k=3))
        random_str=str(random.randint(10,99))+str(code)
        username_=first_name+"@"+random_str
        print(username_)


        curr_user=Account.objects.create_user(email,username=username_,
                                    password=password)
        curr_user.phone_number=mobile_number
        curr_user.first_name=first_name
        curr_user.last_name=last_name
        curr_user.save()

        """Redirect with success message"""
        return redirect('home')
    return render(request,'main/index.html')











@login_required
def verification(request):
    # current_user=Account
    current_user=request.user
    if current_user.is_verify:
        messages.warning(request,'Your Number is already verified...!')
        return redirect('home')

    current_otp = generate_opt()
    # current_otp = 1234
    # send_otp(current_user.phone_number, current_otp)

    otp_input=NumberForm()
    if request.method=="POST":
        otp_input=NumberForm(request.POST or None)
        if otp_input.is_valid():
            number=otp_input.cleaned_data['number']
            if number == current_otp:
                current_user.is_verify=True
                current_user.save()
                messages.warning(request, 'You Have Successfully Verify Your Number .!')
                print("'You Have Successfully Verify Your Number .!", current_otp)
                return redirect('home')
            else:
                messages.warning(request, 'Your Input OTP is invalid')
                print("INVALID OTP",current_otp)
                return redirect('otp_verification')
    context={
        'form':otp_input,
        'object':current_user
    }
    return render(request,'accounts/otp_verification.html',context)

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')



def login_view(request):
    context={}
    redirect_to = request.GET.get('next', '')

    user=request.user
    if user.is_authenticated:
        return redirect('home')

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                if redirect_to == "" or redirect_to is None:
                    return redirect("home")
                return HttpResponseRedirect(redirect_to)

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    if redirect_to != "" or redirect_to is not None:
        context['redirect_to'] = redirect_to

    # print(form)
    return render(request, "accounts/login.html", context)

# 7011101001

@login_required
def updateProfile(request):
    context={
        'user':request.user
    }
    form=UpdateProfileForm()
    if request.POST:
        form=UpdateProfileForm(request.POST or None,request.FILES or None,instance=request.user)
        if form.is_valid():
            # form.initial={
            #     "email":request.POST['email'],
            #     "username":request.POST['username'],
            #     "phone_number":request.POST['phone_number'],
            #     "first_name":request.POST['first_name'],
            #     "last_name":request.POST['last_name'],
            #     "profile_pic":request.FILES['profile_pic'],
            # }
            form.save()
            messages.success(request, "Your Profile is updated successfully")
            context['success_message'] = "Updated"
    else:
        form=UpdateProfileForm(
            initial={
                "email":request.user.email,
                "username":request.user.username,
                "phone_number":request.user.phone_number,
                "first_name":request.user.first_name,
                "last_name":request.user.last_name,
                "profile_pic":request.user.profile_pic,

            }
        )
    context['form'] = form

    return render(request,'accounts/profile_edit.html',context)
