from django import forms
from django_countries.fields import CountryField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout,Submit,Row,Column
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


PAYMENT_METHOD=(
    ('s','strip'),
    ('p','paypal')
)

class CheckoutForm(forms.Form):
    address=forms.CharField( label='Address', widget=forms.TextInput(attrs={
        'placeholder':'e.g-1234'
    }))
    county=forms.CharField(label='County', widget=forms.TextInput(attrs={
        'placeholder':'e.g-1234'
    }))
    country = CountryField(blank_label='select country').formfield()
    same_billing_address=forms.BooleanField(widget=forms.CheckboxInput())
    save_info=forms.BooleanField(widget=forms.CheckboxInput())
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_METHOD)


class SignUpForm(UserCreationForm):
    email=forms.CharField(max_length=250,
                required=True,
                label='Email', 
                widget=forms.EmailInput(
                    attrs= {'placeholder':"Enter Mobile number or Email"} )
                )
    full_name=forms.CharField(label='Full Name',
                max_length=250,
                required=True,
                widget=forms.TextInput(attrs= {
                    'placeholder':"Enter Full Name"})
                )
    username=forms.CharField(label='Username',
                max_length=250,
                required=True,
                widget=forms.TextInput(attrs= {
                    'placeholder':"Enter Username"})
                )
    password1=forms.CharField( label='Password' ,
                max_length=250,
                required=True,
                widget=forms.PasswordInput(attrs= {
                    'placeholder':"Enter Password"})
                )
    password2=forms.CharField(label='Confirm Password',
                max_length=250,
                required=True,
                widget=forms.PasswordInput(attrs= {
                    'placeholder':"Confirm password"})
                )
    class Meta:
        model=User
        fields=('email','full_name','username','password1','password2')


