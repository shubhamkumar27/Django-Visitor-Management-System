from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth.decorators import login_required
from accounts.models import Host

## Homepage
def home(request):
    return render(request, 'homepage.html')

## Doctors details for visitors
def doctors(request):
    hosts = Host.objects.all()
    parameters = {'hosts':hosts}
    return render(request,'doctors.html',parameters)

## Login page for admin
def loginPage(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/dashboard")
        else:
            return redirect('/admin_login/')

    else:
        return render(request,'admin_login.html')
        

