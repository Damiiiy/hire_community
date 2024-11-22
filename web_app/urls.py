from django.urls import path
from web_app.views import *
from django.conf import settings  
from django.conf.urls.static import static



urlpatterns = [
 path('', index, name='index'), 
 path('login', login_view, name='login'),
 path('logout', signout, name='logout'),
 path('User-information', User_sign_up, name='signup'),
 path('User-Profile', Profile_sign_up, name='profile-registration'),

 path('Dashboard', profile_view, name='profile'), 


#  job-seeker
 path('Manage-application', manage_application, name='manage_application'),
#  path('Add-Resume', add_resume, name='add_resume'),
 path('Basic-informations', resume_basic_info, name='resume_basic'),
 path('Education-informations', resume_Edu_info, name='add_resume2'),
 path('Work-information', resume_Work_info, name='add_resume3'),
 path('Skill-information', resume_skill_info, name="add_resume4" ),


# Employer
 path('add-job', add_job, name='add_job'),



#  path('adding-resume', resume_form , name='adding_resume'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

