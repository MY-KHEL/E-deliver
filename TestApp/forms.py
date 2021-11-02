from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import fields
from phonenumber_field.formfields import PhoneNumberField


class signupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields=[
            'first_name',
            'last_name',
            'username',
            'email',
            'image',
            'phone_number',
            'password1',
            'password2',
            'address',
        ]

# class CustomUserCreationForm(UserCreationForm):
#     class Meta:
#         model = CustomUser
#         fields = [
#             'first_name',
#             'last_name',
#             'username',
#             'email',
#             'image',
#             'password1',
#             'password2',
#         ]

class MailForm(forms.ModelForm):
    recipent_phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Enter in this format +Country code')}), required=False)
    Phone_Number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Enter in this format +Country code')}), required=False)
    class Meta:
        model = Mail
        fields = [
            "first_name",
            "last_name",
            "Phone_Number",
            "recipent_first_name",
            "recipent_last_name",
            "recipent_phone_number",
            "Address",
            'receiver_city'
        ]
class PickupMailForm(forms.ModelForm):

    Phone_Number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Enter in this format +Country code')}), 

                       label=("Phone number"), required=False)
    recipent_phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Enter in this format +Country code')}),  required=False)
    class Meta:
        model = Mail
        fields = [
            "first_name",
            "last_name",
            "Phone_Number",
            "Sender_Address",
            'sender_city',
            "recipent_first_name",
            "recipent_last_name",
            "recipent_phone_number",
            "Address",
            'receiver_city'
        ]

class Reassign(forms.ModelForm):
    class Meta:
        model = AssignMail
        fields=[
            "riderid"     
        ]


class Deliver(forms.ModelForm):
    receiver_phone_number = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': ('Enter in this format +Country code')}), 

                       label=("Phone number"), required=False)
        
    class Meta:
        model = DeliveryForm
        fields =[
            "receiver_first_name",
            "receiver_last_name",
            "receiver_phone_number",
            "mail"
        ]
        # widgets = {
        #     'mail': Textarea(attrs={'cols': 80, 'rows': 20}),
        # }

class PaymentForm(forms.ModelForm):

    class Meta:
        model = Payment 
        fields = [
            
            'amount',
            'email'
        ]

class ComplaintForm(forms.ModelForm):
    email = forms.EmailField()
    complaint = forms.Textarea()

    class Meta:
        model=Complaint
        fields=[
            'first_name',
            'last_name',
            'email',
            'complaint',
        ]
        
class CityForm(forms.ModelForm):
    class Meta:
       model = City
       fields=[
           'Name',
           'Price'
       ]       