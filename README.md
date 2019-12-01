# Summergeeks : HealthPlus-Visitor-Management-System
A Visitor Management Web App made using Django.

This is a simple web application which can be used for managing meetings and visitor details. It can keep track of all the meetings and can send emails and sms to host and visitor about their meeting details.

Being a web application it also serves as an organisation's official website where other people can visit and get more information about the organisation.

#### This project is made by keeping a healthcare organisation in mind. Though it can be modified for any organisation.

#### Why i made it organisation specific?
Well !, as it also acts as an organisation's official website, so i took an example organisation. Also, its always better to explain with examples : )

## Visit deployed website
- Deployed on pythonanywhere : http://healthplus.pythonanywhere.com/

### Watch Demo video (Recommended)
- Visit - https://youtu.be/qxKQe9csSGA
<a href="https://youtu.be/qxKQe9csSGA" target="_blank"><img src="https://drive.google.com/uc?id=153qoLXimg2ov340O5EDiTG00HD7T5bEU" alt="Demo Video" title="Visitor management system" /></a>

#### Screenshots of Emails and SMS
<img src="https://drive.google.com/uc?id=1-Qjaqkki9E8cOrEBrfzYGVkpB-WCxNaG" alt="Emails and SMS" title="Screenshots" />

## Technology Stack
- Django - Backend
- HTML, CSS, Bootstrap - Frontend
- Sqlite3 - Database
- Jinja - Templating engine
- way2sms Message API (You can use any API of your choice!)

## Approach for developing backend
As there are two major things to store, which are host details and meeting/visitor details. I have created two models for it, named as :

- Host, with following fields:

    + id = `AutoField`
    + host_name = `CharField`
    + host_email = `EmailField`
    + host_phone = `IntegerField`
    + host_image = `ImageField`
    + host_desc = `CharField`
    + address = `CharField`
    + status = `BooleanField`
    + available = `CharField`
    + current_meeting_id = `IntegerField`

- Meeting, with following fields:

    + id = `AutoField`
    + visitor_name = `CharField`
    + visitor_email = `EmailField`
    + visitor_phone = `IntegerField`
    + host = `CharField`
    + date = `DateField`
    + time_in = `TimeField`
    + time_out = `TimeField`
    
These two models are connected using the meeting ID which is stored in both of them, during meeting the status of host is set as busy and after the meeting is over, the meeting Id filled inside current_meeting_id is deleted and host's status is set to free. Also the checkout time is autofilled inside meeting details.

## Features
- Simple and easy to use GUI.
- Faster load speeds (thanks to Django!).
- Password secured admin panel/dashboard.
- Descriptive dashboard that shows all hosts with their images, details and status.
- Keeps track of all meetings and respective visitor details.
- Emails and SMS notification to both visitor and Host.
- Easy to ADD, DELETE or EDIT a host profile.

## Solution Workflow
Let a visitor wants to meet a host, he goes to reception and asks for the same. The receptionist/admin checks for the host on the dashboard. Dashboard shows information of all hosts with their current status. If they are busy it shows the current visitor details and gives a checkout option. If the host is free, admin fills the visitor details in the meeting form and clicks the check-in button. As the button is clicked, a mail and a sms is sent to host informing about visitor details. When the meeting is over, the visitor while going back asks the receptionist for the checkout. After check-out button is clicked, a mail with all details of meeting is sent to visitor's mail id.

## Local Machine development setup
- Clone the repository on your machine 
    ```
    git clone https://github.com/shubhamkumar27/Summergeeks-Visitor-Management-System.git
    ```
    
- Install all dependencies by executing the following command:
    ```
    pip install -r requirements.txt
    ```
    
- You need to make some changes to the settings.py file inside visitor_management folder, go to bottom of the file
    ```
    UPDATE : EMAIL_HOST_USER = "your email id" 
    UPDATE : EMAIL_HOST_PASSWORD = "your email id password"
    ```
    ( Make sure you <a href='https://myaccount.google.com/lesssecureapps'>enable less secure apps</a> in your google account, so that it sends email ! )
   
- Now you need to edit some lines in views.py file inside accounts folder
  - INSIDE email function:
    ```
    UPDATE : sender = 'your email id'
    ```
  - GO to <a href='https://www.way2sms.com/'>way2sms</a>, create your account and genetrate your test apikey and secret key. Now go INSIDE sendsms function:
    ```
    UPDATE : 'apikey':'your api key',
    UPDATE : 'secret':'your secret key',
    UPDATE : 'senderid' : 'your way2sms account email id'
    ```
    
- Now go inside the main folder which was cloned (manage.py file will be present there), now open a terminal in that directory and run follwing commands:
    ```
    python manage.py createsuperuser
    # follow further instruction there
    
    - After super user is created 
    python manage.py makemigrations
    python manage.py migrate
    
    python manage.py runserver
    ```
- Now server will start at - http://127.0.0.1:8000/



## Want to contribute or found any bug ?
- Make sure you raise an issue if you find any error or bug.
- If you want to add any feature or want to fix any issue, please make a pull request.
- Contact me at my mail id - shubhamkumar8180323@gmail.com - for any kind of help.

#### Made with ♥ by `Shubham Kumar`
