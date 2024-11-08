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
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
