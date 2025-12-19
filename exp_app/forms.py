from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *

class RegForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        fields = ['username','email','password1','password2']
        
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['title','amount','transaction_type','date','category']
        
class GoalForm(forms.ModelForm):
    class Meta:
        model = Goal
        fields = ['name','target_amount','deadline']
        


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'phone', 'location', 'profile_image']
        widgets = {
            'profile_image': forms.FileInput(),  # ✅ removes "Currently / Clear"
        }