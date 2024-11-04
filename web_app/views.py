from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from web_app.models import *


# Create your views here.



def index(request):

    return render(request, 'index.html', {'user': request.session})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        # try:
        #     username = request.POST.get('username')
        #     password = request.POST.get('password')
        # except Exception:
        #     return render(request, 'login.html', {'messege': "Username is not a character"})
        
        if not username or not password:
            return render(request, 'login.html', {'messege': "Username and Password IS REQUIRED"})
        else:
            pass
        try:
            user = Users.objects.get(username=username)
        except Users.DoesNotExist:
            return render(request, 'login.html', {'messege': f"Username {username} does not exist"})
                    # Checking if the password matches the password for the username
        if user.password == password:
            request.session['user'] = username
            # this will help when the redirecting url has a parameter 'next'
            new_redirect = request.GET.get('next', 'index')
            return redirect(new_redirect)
        else:
            return render(request ,'login.html', {'messege': 'Invalid username or password'})

    return render(request, 'login.html')




def sign_up(request):


    return render(request, 'signup.html')