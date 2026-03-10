from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser
from portfolio.models import Profile


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-input'
            field.widget.attrs['placeholder'] = field.label


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['headline', 'bio', 'avatar', 'location', 'website', 'github', 'linkedin', 'slug', 'portfolio_visibility']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'avatar':
                field.widget.attrs['class'] = 'form-input'
            else:
                field.widget.attrs['class'] = 'form-file-input'
            field.widget.attrs['placeholder'] = field.label