from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username','email','password1','password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'github', 'linkedin', 'portfolio_visibility']