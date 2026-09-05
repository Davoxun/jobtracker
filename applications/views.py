from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from .models import Application
from .forms import ApplicationForm
# Create your views here.

def userRegister(request):
    if request.method == "GET":
        newForm = UserCreationForm()
        return render(request, 'register.html', {'form': newForm})
    elif request.method == "POST":
        newUser = UserCreationForm(request.POST)
        if newUser.is_valid():
            userConfirm = newUser.save()
            login(request, userConfirm)
            return HttpResponse("Success!")
        else:
            return render(request, 'register.html', {'form' : newUser})

def userLogin(request):
    if request.method == "GET":
        loginForm = AuthenticationForm()
        return render(request, 'login.html', {'form' : loginForm})
    elif request.method == "POST":
        loginForm = AuthenticationForm(data=request.POST)
        print("Form valid?", loginForm.is_valid())
        print("Form errors:", loginForm.errors)
        if loginForm.is_valid():
            user = authenticate(request, username=loginForm.cleaned_data.get('username'), password=loginForm.cleaned_data.get('password'))
            if user != None:
                login(request, user)
                return render(request, 'home.html')
            else:
                return render(request, 'login.html', {'form' : loginForm})
        else:
            return render(request, 'login.html', {'form' : loginForm})


@login_required
def applicationList(request):
    applications = Application.objects.filter(user=request.user)
    return render(request, 'applications.html', {'applications' : applications})

@login_required
def createApplication(request):
    if request.method == "GET":
        new_form = ApplicationForm()
        return render(request, 'create_applications.html', {'form' : new_form})
    elif request.method == "POST":
        new_form = ApplicationForm(request.POST)
        if new_form.is_valid():
            application = new_form.save(commit=False)
            application.user = request.user
            application.save()
            return redirect('applications')
        else:
            return render(request, 'create_applications.html', {'form' : new_form})

def home(request):
    if request.user.is_authenticated:
        return redirect('applications')
    else:
        return render(request, 'home.html')

@login_required
def deleteApplication(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    application.delete()
    return redirect('applications')

@login_required
def editApplication(request, application_id):
    application = get_object_or_404(Application, id=application_id, user=request.user)
    if request.method == "GET":
        edit_form = ApplicationForm(instance=application)
        return render(request, 'create_applications.html', {'form' : edit_form})
    elif request.method == "POST":
        edit_form = ApplicationForm(data=request.POST, instance=application)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('applications')
        else:
            return render(request, 'create_applications.html', {'form' : edit_form})



        
    
