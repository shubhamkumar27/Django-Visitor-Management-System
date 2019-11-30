from django import forms
from .models import *

# Add host profile form
class Add_profile(forms.ModelForm):
    host_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Name'}), required=True, max_length=50)
    host_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Email Id'}), required=True, max_length=50)
    host_phone = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Phone Number'}), required=True, max_length=10)
    host_image = forms.FileField(required = True)
    host_desc = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width : 17rem','placeholder':'Role'}), required=True, max_length=50)
    available = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','style':'width : 28rem','placeholder':'Monday - Friday'}), required=True, max_length=50)

    class Meta():
        model = Host
        fields = ['host_name','host_email','host_phone','host_image','host_desc','available']

# Add a meeting form
class Meeting_form(forms.ModelForm):
    visitor_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'Name'}), required=True, max_length=50)
    visitor_email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control','placeholder':'Email Id'}), required=True, max_length=50)
    visitor_phone = forms.CharField(widget=forms.NumberInput(attrs={'class':'form-control','placeholder':'Phone Number'}), required=True, max_length=10)
    
    class Meta():
        model = Meeting
        fields = ['visitor_name','visitor_email','visitor_phone']