from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from accounts.models import Host

def home(request):
    return render(request, 'homepage.html')

def doctors(request):
    hosts = Host.objects.all()
    parameters = {'hosts':hosts}
    print(hosts) 
    return render(request,'doctors.html',parameters)

def loginPage(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'Invalid credentials !!')
            return redirect('login')

    else:
        return render(request,'admin_login.html')

@login_required(login_url='/admin_login/')
def logout(request):
    auth.logout(request)
    return redirect('/')

