from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *



class UserForm(forms.ModelForm):
    first_name = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )

    last_name = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
    )
    username = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )

    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )
    
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password']




class ProfileForm(forms.ModelForm):
    USER_TYPE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES, 
        widget=forms.RadioSelect(attrs={'class': 'form-check-input', "style" : 'red' }),
        label="I am a"
    )
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Tell us about yourself'}),
        required=False
    )
    location = forms.CharField(
        max_length=255, 
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    website = forms.URLField(
        required=False, 
        help_text="For employers only.",
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website URL'})
    )
  
    class Meta:
        model = Profile
        fields = ['user_type', 'bio', 'location', 'profile_picture', 'website']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            
        }
    