from django.urls import path
from web_app.views import *



urlpatterns = [
 path('', index, name='index'), 
 path('login', login_view, name='login'),
 path('signup', sign_up, name='signup'),
 
]
