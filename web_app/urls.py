from django.urls import path
from web_app.views import *
from django.conf import settings  
from django.conf.urls.static import static



urlpatterns = [

 #########################b ACCOUNTS ##############################
 path('', index, name='index'), 
 path('login', login_view, name='login'),
 path('logout', signout, name='logout'),
 path('user-information', User_sign_up, name='signup'),
 path('user-Profile', Profile_sign_up, name='profile-registration'),


#################### EMPLOYER #########################

 path('dashboard/', profile_view, name='profile'),
 path('job-details/<int:job_id>', job_details, name='job_details'),
 path('browse-jobs/<str:category_name>/', browse_jobs, name='browse_jobs'),
 path('add-job', add_job, name='add_job'),
 path('skilled-Jobs/', post_skilled_job, name='skilled-jobs'),
 path('unskilled-job', post_skilled_job, name='unskilled-jobs'),

 ###############  job-seeker ############################
 path('manage-application', manage_application, name='manage_application'),
#  path('Add-Resume', add_resume, name='add_resume'),
 path('basic-informations', resume_basic_info, name='resume_basic'),
 path('education-informations', resume_Edu_info, name='add_resume2'),
 path('work-information', resume_Work_info, name='add_resume3'),
 path('skill-information', resume_skill_info, name="add_resume4" ),


# Employer



#  path('adding-resume', resume_form , name='adding_resume'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

