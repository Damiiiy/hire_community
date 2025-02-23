from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.forms import modelformset_factory

from .models import *

class UserForm(UserCreationForm):
    # email = forms.EmailField(required=True)
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

    email = forms.EmailField(
        required=True,
        help_text="Required. Enter a valid email address.",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
    )

    password2 = forms.CharField(
        label=" Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
    )

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

# class UserForm(forms.ModelForm):
#     first_name = forms.CharField(
#         required=True,
#         help_text="Required.",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
#     )
#
#     last_name = forms.CharField(
#         required=True,
#         help_text="Required.",
#         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'})
#     )
#
#
#     email = forms.EmailField(
#         required=True,
#         help_text="Required. Enter a valid email address.",
#         widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
#     )
#
#     password = forms.CharField(
#         label="Password",
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
#     )
#
#
#     class Meta:
#         model = CustomUser
#         fields = ['first_name', 'last_name', 'email', 'password']

class LoginForm(AuthenticationForm):
    email = forms.EmailField(
            widget=forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email',
                'autofocus': True,
            }),
            label="Email"
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter Password'})
        )


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
        required=True
    )
    location = forms.CharField(
        max_length=255, 
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    profile_picture = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

  
    class Meta:
        model = Profile
        fields = ['user_type', 'bio', 'location', 'profile_picture']
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



class JobForm(forms.ModelForm):
    title = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title, e.g., UI/UX Researcher'})
    )
    job_tag = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Job's Tag"})
    )
    company_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'})
    )
    location = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'})
    )
    salary = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Salary, e.g., 85'})
    )
    skills_required = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Skills, e.g., HTML'})
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Description of the Job'})
    )
    job_type = forms.ChoiceField(
        required=True,
        choices=Job.JOB_TYPE_CHOICES,  # Fixed the choices reference
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ChoiceField(
        required=True,
        choices=Job.JOB_CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cover_img = forms.ImageField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )

    class Meta:
        model = Job
        fields = [
            'title',
            'job_tag',
            'description',
            'company_name',
            'location',
            'salary',
            'skills_required',
            'job_type',
            'category',
            'cover_img'
        ]




#
# class JobForm(forms.ModelForm):
#     title = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Title, e.g., UI/UX Researcher'
#         })
#     )
#     job_tag = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': "Job's Tag"
#         })
#     )
#     company_name = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Company Name'
#         })
#     )
#     location = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Location'
#         })
#     )
#     salary = forms.IntegerField(
#         required=True,
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Salary, e.g., 85'
#         })
#     )
#     skills_required = forms.CharField(
#         required=True,
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Skills, e.g., HTML'
#         })
#     )
#     description = forms.CharField(
#         required=True,
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'rows': 4,
#             'placeholder': 'Description of the Job'
#         })
#     )
#     job_type = forms.ChoiceField(
#         required=True,
#         choices=Job.JOB_TYPE_CHOICES,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     category = forms.ChoiceField(
#         required=True,
#         choices=Job.JOB_CATEGORY_CHOICES,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#     cover_img = forms.ImageField(
#         required=True,
#         widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
#     )
#
#     class Meta:
#         model = Job
#         fields = [
#             'title',
#             'job_tag',
#             'description',
#             'company_name',
#             'location',
#             'salary',
#             'skills_required',
#             'job_type',
#             'category',
#             'cover_img'
#         ]

############################################################33

#
# class JobForm(forms.ModelForm):
#     title = forms.CharField(
#         required=True,
#         help_text="Required.",
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Title, e.g., UI/UX Researcher'
#         })
#     )
#     job_tag = forms.CharField(
#         required=True,  # Optional field in the model
#         help_text="Optional.",
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': "Job's Tag"
#         })
#     )
#     company_name = forms.CharField(
#         required=True,
#         help_text="Required.",
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Company Name'
#         })
#     )
#     location = forms.CharField(
#         required=True,  # Optional field in the model
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Location'
#         })
#     )
#     salary = forms.IntegerField(
#         required=True,  # Optional field in the model
#         widget=forms.NumberInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Salary, e.g., 85'
#         })
#     )
#
#     skills_required = forms.CharField(
#         required=True,  # Optional field in the model
#         help_text="Optional.",
#         widget=forms.TextInput(attrs={
#             'class': 'form-control',
#             'placeholder': 'Skills, e.g., HTML'
#         })
#     )
#     description = forms.CharField(
#         required=True,
#         help_text="Required.",
#         widget=forms.Textarea(attrs={
#             'class': 'form-control',
#             'rows': 4,
#             'placeholder': 'Description of the Job'
#         })
#     )
#     job_type = forms.ChoiceField(
#         required=True,
#         choices=Job.job_type.field.choices,
#         widget=forms.Select(attrs={
#             'class': 'form-control'
#         })
#     )
#
#     category = forms.ChoiceField(
#         choices=Job.JOB_CATEGORY_CHOICES,
#         required=True,
#         widget=forms.Select(attrs={'class': 'form-control'})
#     )
#
#     cover_img = forms.ImageField(
#         required=True,
#         help_text="Optional.",
#         widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
#
#     )
#
#     class Meta:
#         model = Job
#         fields = [
#             'title',
#             'job_tags'
#             'description',
#             'company_name',
#             'location',
#             'salary',
#             'skills_required',
#             'job_type',
#             'category',
#             'cover_img'
#         ]
