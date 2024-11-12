from django import forms
from django.forms import modelformset_factory

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
    



 ############# resume form data #############
class ResumeProfileForm(forms.ModelForm):
    name = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
    )
    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'your@email.com'})
    )
    profession_title = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Headline (e.g. Front-end developer)'})
    )
    location = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    web = forms.URLField(
        label="Password",
        widget=forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Website address'})
    )
    per_hour = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary, e.g. 85'})
    )
    age = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Age'})
    )

    class Meta:
        model = ResumeProfile
        fields = ['name', 'email', 'profession_title', 'location', 'web', 'per_hour', 'age']

class EducationForm(forms.ModelForm):
    degree = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Degree'})
    )
    field_of_study = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Major, e.g Computer Science'})
    )
    school = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'School'})
    )
    start_year = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Started at'})
    )
    end_year = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ended at'})
    )
    description = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows':'4', 'placeholder': 'Description'})
    )
    class Meta:
        model = Education
        fields = ['degree', 'field_of_study', 'school', 'start_year', 'end_year', 'description']

class ExperienceForm(forms.ModelForm):
    company_name = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'})
    )
    title = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title, e.g UI/UX Researcher'})
    )
    work_start_year = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Start at'})
    )
    work_end_year = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ended at'})
    )
    work_description = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': '4',  'placeholder': 'Work Description'})
    )
    class Meta:
        model = Experience
        fields = ['company_name', 'title', 'work_start_year', 'work_end_year', 'work_description']

class SkillForm(forms.ModelForm):
    skill_name = forms.CharField(
        required=True,
        help_text="Required.",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skill Name, e.g. HTML'})
    )
    proficiency = forms.IntegerField(
        required=True,
        help_text="Required.",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Skill proficiency, e.g. 90'})
    )
    class Meta:
        model = ResumeSkill
        fields = ['skill_name', 'proficiency']

# Create formsets for each repeating section
