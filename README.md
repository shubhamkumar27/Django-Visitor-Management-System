# HealthPlus-Visitor-Management-System
A Visitor Management Web App made using Django.

This is a simple web application which can be used for managing meetings and visitor details. It can keep track of all the meetings and can send emails and sms to host and visitor about their meeting details.

Being a web application it also serves as an organisation's official website where other people can visit and get more information about the organisation.

This project is made by keeping a healthcare organisation in mind. Though it can be modified for any organisation.

#### Why i made it organisation specific?
Well!, as it also acts as an organisation's official website, so i took an example organisation. Also, its always better to explain with examples ;)

## Technology Stack
- Django (Backend)
- HTML, CSS, Bootstrap (Frontend)
- Sqlite3 (Database)
- way2sms Message API (You can use any API of your choice!)

## Approach for developing backend
As there are two major things to store, which are host details and meeting/visitor details. I have created two models for it, named as 'Host' and 'Meeting'. These two models are connected using the meeting ID which is stored in both of them, during meeting the status of host is set as busy and after the meeting is over, the meeting Id filled inside 'Host' is deleted and host's status is set to free. Also the checkout time is autofilled inside meeting details.

## Features
- Simple and easy to use GUI.
- Faster load speeds (thanks to Django!).
- Password secured admin panel/dashboard.
- Descriptive dashboard which shows all hosts with their details and status.
- Keeps track of all meetings and respective visitor details.
- Emails and SMS notification to both visitor and Host.
- Easy to add, delete or edit a host profile.

## Solution Workflow
Let a visitor wants to meet a host, he goes to reception and asks for the same. The receptionist/admin checks for the host on the dashboard. If the host is free, admin fills the visitor details in the meeting form and clicks the check-in button. As the button is clicked, a mail and a sms is sent to host informing about visitor details. When the meeting is over, the visitor while going back asks the receptionist for the checkout. After check-out button is clicked, a mail with all details of meeting is sent to visitor's mail id.

## Demo of deployed web app.
- http://healthplus.pythonanywhere.com/
