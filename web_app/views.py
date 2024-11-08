from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from web_app.models import *
from django.contrib import messages
from web_app.forms import *



# Create your views here.



def index(request):
    if 'user' in request.session:
        user = request.session['user']
        users = CustomUser.objects.get(username=user)
            # userid = CustomUser.objects.get(id=users)
        
        
        profile = Profile.objects.get(user=users) 

        return render(request, 'index.html', {'user': user, 'profile': profile})
    else:
        return render(request, 'index.html')

def profile_view(request):
    if 'user' in request.session:
        user = request.session['user']
        users = CustomUser.objects.get(username=user)

        # get profile information
        profile = Profile.objects.get(user=users) 
        return render(request, 'profile.html', {'user': users, 'profile':profile})
    else:
        return redirect('login')
                  
def login_view(request):
    if 'user' in request.session:
        return redirect('index')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            if not username or not password:
                return render(request, 'login.html', {'messege': "Username and Password IS REQUIRED"})
            else:
                pass
            try:
                user = CustomUser.objects.get(username=username)
            except CustomUser.DoesNotExist:
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

def signout(request):
    if request.session.has_key('user'):
        del request.session['user']
    return redirect('index')

def User_sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            
            # Save form data to session and proceed to Step 2
            request.session['user_form_data'] = form.cleaned_data
            return redirect('profile-registration')
        else:
            print(form.cleaned_data)
            print(form.errors)
            messages.error(request, form.errors)
    else:
        form = UserForm() 
    return render(request, 'signup.html', {'form': form})

def Profile_sign_up(request):
    user_form_data = request.session.get('user_form_data')
    if not user_form_data:
        # return redirect('signup')  # Redirect to Step 1 if no data in session
        return render(request, 'signup.html', {'form': form, 'error': 'False'})

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Create User and Profile instances
            user = CustomUser(
                username=user_form_data['username'],
                first_name=user_form_data['first_name'],
                last_name=user_form_data['last_name'],
                email=user_form_data['email'],
                password=user_form_data['password']
            )
            user.save()
            
          
            # Manually create and save the Profile instance
            profile = Profile(
                user=user,
                user_type=form.cleaned_data['user_type'],
                bio=form.cleaned_data['bio'],
                location=form.cleaned_data['location'],
                profile_picture=form.cleaned_data['profile_picture'],
                website=form.cleaned_data['website']
            )
            profile.save()

            # Log in the user and clear session data
            # login(request, user)
            request.session.pop('user_form_data', None)  # Clear session after registration
            messages.success(request, "Registration successful!")
            return redirect('home')
        else:
            messages.error(request, form.errors)
    else:
        form = ProfileForm() 
    return render(request, 'signup2.html', {'form': form})



# def sign_up(request):


#     return render(request, 'signup.html')