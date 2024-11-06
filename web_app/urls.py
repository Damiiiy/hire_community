from django.urls import path
from web_app.views import *



urlpatterns = [
 path('', index, name='index'), 
 path('login', login_view, name='login'),
 path('User-information', User_sign_up, name='signup'),
 path('User-Profile', Profile_sign_up, name='profile'),
 
]
