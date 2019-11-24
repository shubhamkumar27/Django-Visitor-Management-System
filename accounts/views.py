from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.decorators import login_required
from .models import Host, Meeting
from pushbullet import PushBullet
from .forms import *
import datetime


# Create your views here.
@login_required(login_url='/admin_login/')
def dashboard(request):
    h = Host.objects.all()
    hosts = sorted(list(h),key=lambda x: x.host_name)
    parameters = {'hosts':hosts}
    return render(request,'dashboard.html',parameters)

@login_required(login_url='/admin_login/')
def meeting_manager(request):
    if request.method == 'POST':

        if request.POST.get("visitor"):
            meeting_id = request.POST.get("visitor")
            meeting = Meeting.objects.get(id = meeting_id)
            host = Host.objects.get(current_meeting_id = meeting_id)
            meeting_details = {'meeting' : meeting, 'host' : host}
            return render(request, 'visitor_details.html', meeting_details)

        elif request.POST.get("check_out"):
            m_id = request.POST.get("check_out")
            meeting = Meeting.objects.get(id = m_id)
            host = Host.objects.get(current_meeting_id=m_id)
            host.status = True
            host.current_meeting_id = None 
            meeting.time_out = datetime.datetime.now()
            host.save()
            meeting.save()
            rec = [meeting.visitor_email]
            Subject = "HealthPlus Meeting Details"
            visitor = meeting
            email(Subject,visitor,rec,host)
            return redirect('/dashboard')

        elif request.POST.get("meeting"):
            host_id = request.POST.get("meeting")
            host = Host.objects.get(id = host_id)
            form = Meeting_form()
            param = {'form':form,'host':host}
            return render(request, 'meeting_form.html', param)
    else:
        return redirect('/dashboard')

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
            subject = "Visitor Information"
            visitor = instance
            email(subject,visitor,rec)
            sms(subject,visitor,host)
    return redirect('/dashboard')

@login_required(login_url='/admin_login/')
def meeting_history(request):
    meetings = Meeting.objects.filter(date = datetime.datetime.now())
    m = reversed(list(meetings))
    info = {'meeting':m}
    return render(request, 'meeting_history.html',info)

@login_required(login_url='/admin_login/')
def profile_manager(request):
    if request.method=='POST':
        form = Add_profile(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('/dashboard')
    else:
        form = Add_profile()
        return render(request, 'profile_manager.html', {'form' : form})

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
        return redirect('/dashboard/profile_manager')

@login_required(login_url='/admin_login/')
def edit_delete(request):
    if request.method=='POST':
        host_id =request.POST.get('id')
        host = Host.objects.filter(id=host_id).first()
        if host:
            if request.POST.get('edit'):
                form = Add_profile(instance=host)
                context = {'form':form,'edit':True,'info':host_id}
                return render(request, 'profile_manager.html',context)
            elif request.POST.get('delete'):
                host.delete()
                return redirect('/dashboard')
        return redirect('/dashboard/profile_manager')
    else:
        return redirect('/dashboard/profile_manager')

def email(subject,visitor,rec,host=None):
    sender = 'healthplusnotification@gmail.com'
    if host:
        html_content = render_to_string('visitor_mail_template.html', {'visitor':visitor,'host':host}) # render with dynamic value
    else:
        html_content = render_to_string('host_mail_template.html', {'visitor':visitor}) # render with dynamic value
    text_content = strip_tags(html_content)
    try:
        msg = EmailMultiAlternatives(subject, text_content, sender, rec)
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except:
        pass
    return

def sms(subject,visitor,host):
    msg = "Hey, "+host.host_name+", Your Upcoming meeting is with : "+visitor.visitor_name+", Contact no. : "+str(visitor.visitor_phone)+", Email Id : "+visitor.visitor_email+". Check-In Time is : "+str(visitor.time_in)[11:16]
    rec = '+91'+str(host.host_phone)
    try:
        p =  PushBullet('o.0CZaKLWsOzzEfG7kACoZ8paOeun5ecep')
        p.push_sms(p.devices[0],rec,msg)
    except:
        pass
    return