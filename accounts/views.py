from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Host, Meeting
from .forms import *
import datetime
import requests
import json

# Create your views here.

@login_required(login_url='/admin_login/')
def dashboard(request):
    h = Host.objects.all()
    hosts = sorted(list(h),key=lambda x: x.host_name)
    parameters = {'hosts':hosts}
    return render(request,'dashboard.html',parameters)

## Verifies that only Admin uses these options and redirects them to required webpage respectively
def verify(request):
    if request.method == 'POST':
        key = request.POST.get('password')
        user = auth.authenticate(username=request.user.username,password=key)
        if user is not None:
            if request.POST.get('profile'):
                form = Add_profile()
                return render(request, 'profile_manager.html', {'form' : form})

            if request.POST.get('logout'):
                auth.logout(request)
                return redirect('/')

            if request.POST.get('meeting'):
                meetings = Meeting.objects.filter(date = datetime.datetime.now())
                m = reversed(list(meetings))
                info = {'meeting':m}
                return render(request, 'meeting_history.html',info)
        
        # When wrong password is given
        else:
            messages.warning(request,'Please enter valid credentials !!')
            return redirect('/dashboard')

    else:
        return redirect('/dashboard')

@login_required(login_url='/admin_login/')
def meeting_manager(request):
    if request.method == 'POST':

        # If visitor button is clicked, visitor details are shown
        if request.POST.get("visitor"): 
            meeting_id = request.POST.get("visitor")
            meeting = Meeting.objects.get(id = meeting_id)
            host = Host.objects.get(current_meeting_id = meeting_id)
            meeting_details = {'meeting' : meeting, 'host' : host}
            return render(request, 'visitor_details.html', meeting_details)

        # Opens the meeting form
        elif request.POST.get("meeting"): 
            host_id = request.POST.get("meeting")
            host = Host.objects.get(id = host_id)
            form = Meeting_form()
            param = {'form':form,'host':host}
            return render(request, 'meeting_form.html', param)

    else:
        return redirect('/dashboard')

# Saves the visitor details filled in meeting form
@login_required(login_url='/admin_login/')
def save_meeting(request):
    if request.method == 'POST':
        host_name = request.POST.get('host')
        host = Host.objects.get(host_name=host_name)
        form = Meeting_form(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.time_in = datetime.datetime.now()
            instance.host = host_name
            instance.save()
            host.current_meeting_id = instance.id
            host.status = False
            host.save()
            rec = [host.host_email]
            subject = instance.visitor_name +" Checked In !"
            visitor = instance
            ## EMAIL AND SMS TO HOST
            email(subject,visitor,rec)
            sendsms(subject,visitor,host)
            messages.success(request,'Information sent to Host, You will be called shortly !!')
            return redirect('/dashboard')
        else:
            pass
    else:
        return redirect('/dashboard')

## Checkout function when Host clicks checkout button
def checkout(request):
    if request.method == 'GET':
        meeting_id = request.GET['mid']
        meeting = Meeting.objects.get(id = meeting_id)
        host = next(iter(Host.objects.filter(current_meeting_id=meeting_id)), None)
        # If checkout button already clicked
        if (meeting.time_out != None) and (host==None):
            return HttpResponse(meeting.visitor_name+', Already Checked Out !!')
        host.status = True
        host.current_meeting_id = None 
        meeting.time_out = datetime.datetime.now()
        host.save()
        meeting.save()
        rec = [meeting.visitor_email]
        Subject = "HealthPlus Meeting Details"
        visitor = meeting
        # sending email to visitor
        email(Subject,visitor,rec,host)
        return HttpResponse(meeting.visitor_name+', Checked Out Successfully !!')

# profile manager that saves host profile
@login_required(login_url='/admin_login/')
def profile_manager(request):
    if request.method=='POST':
        form = Add_profile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

# Checks for the given id in host database and fills the add profile form automatically with it
@login_required(login_url='/admin_login/')
def edit_profile(request):
    if request.method == 'POST':
        host_id = request.POST.get('editing')
        instance = Host.objects.filter(id=host_id).first()
        form = Add_profile(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        return redirect('/dashboard')

# checks which button was clicked, either edit or delete and redirects them respectively
@login_required(login_url='/admin_login/')
def edit_delete(request):
    if request.method=='POST':
        host_id =request.POST.get('id')
        if host_id=='':
            # If invalid profile id was given
            messages.warning(request,'Please enter a valid profile Id first !!')
            form = Add_profile()
            return render(request, 'profile_manager.html', {'form' : form})
        host = Host.objects.filter(id=host_id).first()
        if host:
            if request.POST.get('edit'):
                form = Add_profile(instance=host)
                context = {'form':form,'edit':True,'info':host_id}
                return render(request, 'profile_manager.html',context)
            elif request.POST.get('delete'):
                host.delete()
                return redirect('/dashboard')
        else:
            # If no profile was found
            messages.warning(request,'Profile not found !!')
            form = Add_profile()
            return render(request, 'profile_manager.html', {'form' : form})
    else:
        return redirect('/dashboard')


# Sends the email to both host and visitor
def email(subject,visitor,rec,host=None):
    ## FILL IN YOUR DETAILS HERE
    sender = 'your email id'
    if host:
        html_content = render_to_string('visitor_mail_template.html', {'visitor':visitor,'host':host}) # render with dynamic value
    else:
        html_content = render_to_string('host_mail_template.html', {'visitor':visitor}) # render with dynamic value
    text_content = strip_tags(html_content)

    # try except block to avoid wesite crashing due to email error
    try:
        msg = EmailMultiAlternatives(subject, text_content, sender, rec)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        pass
    return

# Sends the SMS to host
def sendsms(subject,visitor,host):
    URL = 'https://www.way2sms.com/api/v1/sendCampaign'
    msg = "Hey, "+host.host_name+", Your Upcoming meeting is with : "+visitor.visitor_name+", Contact no. : "+str(visitor.visitor_phone)+", Email Id : "+visitor.visitor_email+". Check-In Time is : "+str(visitor.time_in)[11:16]
    ## FILL IN YOUR DETAILS HERE
    req_params = {
    'apikey':'your api key',
    'secret':'your secret key',
    'usetype':'stage',
    'phone': '+91'+str(host.host_phone),
    'message':msg,
    'senderid':'your way2sms account email id'
    }
    # try except block to avoid wesite crashing due to SMS error
    try:
        requests.post(URL, req_params)
    except:
        pass
    return
