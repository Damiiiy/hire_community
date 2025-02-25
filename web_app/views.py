from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory
from web_app.models import *
from django.contrib import messages
from django.forms import ValidationError
from web_app.forms import *
import random

# Create your views here.

def index(request):
    jobs = list(Job.objects.all())  # Get all houses as a list
    random.shuffle(jobs)  # Shuffle the list randomly

    categories = Category.objects.all()  # Fetch all categories
    category_counts = {category.name: Job.objects.filter(category=category).count() for category in categories}

    # Split skills in the view
    for job in jobs:
        job.skills_list = job.skills_required.split(",") if job.skills_required else []

    if request.user.is_authenticated:
        user = request.user
        users = CustomUser.objects.get(email=user)

        # get profile information
        profile, created = Profile.objects.get_or_create(user=request.user)

        return render(request, 'index.html', {'user': user, 'profile': profile , 'jobs': jobs,  'categories': categories, 'category_counts': category_counts  })
    else:
        return render(request, 'index.html', {'jobs': jobs, 'categories': categories, 'category_counts': category_counts })
    

def profile_view(request):
    if request.user.is_authenticated:
        user = request.user.email
        users = CustomUser.objects.get(email=user)

        # get profile information
        profile, created = Profile.objects.get_or_create(user=request.user)

        # profile = Profile.objects.get(user=request.user)
        if profile.user_type == "job_seeker":
            try:
                resume = ResumeProfile.objects.get(user=users)
            except ResumeProfile.DoesNotExist:
                # Handle the case where the profile does not exist
                return render(request, 'profile.html', {'user': users, 'profile':profile,})
    #   Continue with the logic if the profile exists
            
            resume = ResumeProfile.objects.get(user=users)
            work_xp = Experience.objects.filter(profile=resume)
            edu_xp = Education.objects.filter(profile=resume)
            skils = ResumeSkill.objects.filter(profile=resume)
            return render(request, 'profile.html', {'user': users, 'profile':profile,'resume':resume, 'work_xp':work_xp, 'edu_xp':edu_xp, 'skills':skils})
            
        if profile.user_type == "employer":
            form = JobForm()
            if request.method == 'POST':
                form = JobForm(request.POST, request.FILES)

                if form.is_valid():
                    try:
                        new_job = Job(
                            category=form.cleaned_data['category'].title(),
                            title=form.cleaned_data['title'].title(),
                            description=form.cleaned_data['description'].capitalize(),
                            employer=users,
                            location=form.cleaned_data['location'].title(),
                            salary=form.cleaned_data['salary'],
                            skills_required=form.cleaned_data['skills_required'].title(),
                            job_tag=form.cleaned_data['job_tag'].title(),
                            job_type=form.cleaned_data['job_type'].title(),
                            cover_img=form.cleaned_data['cover_img']
                        )

                        new_job.save()
                        messages.success(request, "Job created successful!")

                        return redirect('profile')
                    except Exception:
                        messages.error(request, form.errors)

                else:
                    messages.error(request, form.errors)

            

            return render(request, 'profile.html', {'user': users, 'profile':profile, 'form':form})
        return render(request, 'profile.html', {'user': users, 'profile':profile})
    else:
        return redirect('login')
    

    
def manage_application(request):
    if request.user.is_authenticated:
        user = request.user
        users = CustomUser.objects.get(email=user)


        profile, created = Profile.objects.get_or_create(user=request.user)
        return render(request, 'jobseeker/manage_applications.html', {'user': users, 'profile':profile} )
    

    else:
        return redirect('index')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')

    form = LoginForm()
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(email , password)

        if not email or not password:
            return render(request, 'login.html', {'message': "Email and Password are required"})

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            new_redirect = request.GET.get('next', 'index')
            return redirect(new_redirect)
        else:
            return render(request, 'login.html', { 'form':form, 'message': 'Invalid email or password'})

    return render(request, 'login.html', {'form':form})


# def login_view(request):
#     if 'user' in request.session:
#         return redirect('index')
#     else:
#         if request.method == 'POST':
#             username = request.POST.get('email')
#             password = request.POST.get('password')
#             if not username or not password:
#                 return render(request, 'login.html', {'messege': "Username and Password IS REQUIRED"})
#             else:
#                 pass
#             try:
#                 user = CustomUser.objects.get(username=username)
#             except CustomUser.DoesNotExist:
#                 return render(request, 'login.html', {'messege': f"Username {username} does not exist"})
#                         # Checking if the password matches the password for the username
#             if user.password == password:
#                 request.session['user'] = username
#                 # this will help when the redirecting url has a parameter 'next'
#                 new_redirect = request.GET.get('next', 'index')
#                 return redirect(new_redirect)
#             else:
#                 return render(request ,'login.html', {'messege': 'Invalid username or password'})
#
#         return render(request, 'login.html')

def signout(request):
    logout(request)
    return redirect('index')


def User_sign_up(request):
    if request.user.is_authenticated:
        return redirect(index)

    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            # Save form data to session and proceed to Step 2
            request.session['user_form_data'] = form.cleaned_data
            return redirect('profile-registration')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserForm()
    return render(request, 'signup.html', {'form': form})


def Profile_sign_up(request):
    if request.user.is_authenticated:
        return redirect(index)

    user_form_data = request.session.get('user_form_data')
    if not user_form_data:
        messages.error(request, "User form data not found. Please complete Step 1.")
        return redirect('signup')

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            # Check if user already exists
            if CustomUser.objects.filter(email=user_form_data['email']).exists():
                messages.error(request, "User already exists.")
                return render(request, 'signup2.html', {'form': form})

            # Create User instance
            user = CustomUser.objects.create_user(
                first_name=user_form_data['first_name'].capitalize(),
                last_name=user_form_data['last_name'].capitalize(),
                email=user_form_data['email'],
                password=user_form_data['password1']
            )

            # Create and save the Profile instance
            profile = Profile(
                user=user,
                user_type=form.cleaned_data['user_type'],
                bio=form.cleaned_data['bio'].capitalize(),
                location=form.cleaned_data['location'].title(),
                profile_picture=form.cleaned_data['profile_picture'],
            )
            profile.save()

            # Log in the user and clear session data
            # login(request, user)
            request.session.pop('user_form_data', None)  # Clear session after registration
            messages.success(request, "Registration successful!")
            return redirect('index')  # Redirect to home or dashboard

        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileForm()

    return render(request, 'signup2.html', {'form': form})


#
# def User_sign_up(request):
#     if request.method == "POST":
#         form = UserForm(request.POST)
#         if form.is_valid():
#
#             # Save form data to session and proceed to Step 2
#             request.session['user_form_data'] = form.cleaned_data
#             return redirect('profile-registration')
#         else:
#             messages.error(request, form.errors)
#     else:
#         form = UserForm()
#     return render(request, 'signup.html', {'form': form})
#
# def Profile_sign_up(request):
#     user_form_data = request.session.get('user_form_data')
#     if not user_form_data:
#         # return redirect('signup')  # Redirect to Step 1 if no data in session
#         return render(request, 'signup.html', {'form': form, 'error': 'False'})
#
#     if request.method == 'POST':
#         form = ProfileForm(request.POST, request.FILES)
#         if form.is_valid():
#             # Create User and Profile instances
#             user = CustomUser(
#                 first_name=user_form_data['first_name'].capitalize(),
#                 last_name=user_form_data['last_name'].capitalize(),
#                 email=user_form_data['email'],
#                 password=user_form_data['password1']
#
#             )
#
#
#
#             # Manually create and save the Profile instance
#             profile = Profile(
#                 user=user,
#                 user_type=form.cleaned_data['user_type'],
#                 bio=form.cleaned_data['bio'].capitalize(),
#                 location=form.cleaned_data['location'].title(),
#                 profile_picture=form.cleaned_data['profile_picture'],
#             )
#
#             i = CustomUser.objects.all()
#             if user_form_data in i:
#                 messages.error(request, "User Exist ALready")
#                 return render(request, 'signup2.html', {'form': form})
#             else:
#                 user.save()
#                 profile.save()
#                 # Log in the user and clear session data
#                 # login(request, user)
#                 request.session.pop('user_form_data', None)  # Clear session after registration
#                 messages.success(request, "Registration successful!")
#                 return render(request, 'signup2.html', {'form': form})
#
#         else:
#             messages.error(request, form.errors)
#     else:
#         form = ProfileForm()
#     return render(request, 'signup2.html', {'form': form})
#


################## RESUME DATA VIEW ##################

def resume_basic_info(request):
    if not request.user.is_authenticated:
        return redirect('index')
    
    user = request.session['user']
    users = CustomUser.objects.get(username=user)
    profile = Profile.objects.get(user=users)

    profile_form = ResumeProfileForm()

    if request.method == "POST":
        form = ResumeProfileForm(request.POST)
        if form.is_valid():
            
            # Save form data to session and proceed to Step 2
            request.session['resume_basic_form'] = form.cleaned_data
            return redirect('add_resume2')
        else:
            messages.error(request, form.errors)
    else:
        form = UserForm() 
    return render(request, 'jobseeker/add_resume.html', {'profile':profile, 
                                                         'form':profile_form,
                                                         'user':users})
def resume_Edu_info(request):
    if 'user' not in request.session:
        return redirect('index')
    
    user = request.session['user']
    users = CustomUser.objects.get(username=user)
    profile = Profile.objects.get(user=users)

    education_Form = EducationForm ()
    resume_basic_form = request.session.get('resume_basic_form')
    if not resume_basic_form:
        return redirect('resume_basic')  
    
    # print(resume_basic_form)
    if request.method == "POST":
        form = EducationForm(request.POST)
        if form.is_valid():
            
            # Save form data to session and proceed to Step 2
            request.session['user_form_data-edu'] = form.cleaned_data
            return redirect('add_resume3')
        else:
            messages.error(request, form.errors)
    else:
        form = UserForm() 
    return render(request, 'jobseeker/resume_education.html', {'profile':profile, 
                                                         'e_form':education_Form,
                                                         'user':users})

def resume_Work_info(request):
    if 'user' not in request.session:
        return redirect('index')
    
    user = request.session['user']
    users = CustomUser.objects.get(username=user)
    profile = Profile.objects.get(user=users)

    experience_form = ExperienceForm()
    resume_edu_form = request.session.get('user_form_data-edu')
    if not resume_edu_form:
        return redirect('resume_basic')  
    
    # print(resume_edu_form)
    if request.method == "POST":
        form = ExperienceForm(request.POST)
        if form.is_valid():
            
            # Save form data to session and proceed to Step 2
            request.session['user_form_data-work'] = form.cleaned_data
            return redirect('add_resume4')
        else:
            messages.error(request, form.errors)
    else:
        form = UserForm() 
    return render(request, 'jobseeker/resume_experience.html', {'profile':profile, 
                                                         'w_form': experience_form,
                                                         'user':users})

def resume_skill_info(request):
    if 'user' not in request.session:
        return redirect('index')
    
    user = request.session['user']
    users = CustomUser.objects.get(username=user)
    profile = Profile.objects.get(user=users)

    skill_form = SkillForm()

    # lists of form data stored in the session 
    resume_basic_form = request.session.get('resume_basic_form')
    resume_edu_form = request.session.get('user_form_data-edu')
    user_form_data_work = request.session.get('user_form_data-work')

    # checking if previous form data is available

    if not resume_edu_form:
        return redirect('add_resume3')  
    
    # print(resume_edu_form)
    if request.method == "POST":
        form = SkillForm(request.POST)

        if form.is_valid():
             # Create User and Profile instances
            try:
                resume = ResumeProfile(
                    user=users,
                    name=resume_basic_form['name'].title(),
                    email=resume_basic_form['email'],
                    profession_title=resume_basic_form['profession_title'].title(),
                    location=resume_basic_form['location'].title(),
                    web=resume_basic_form['web'],
                    per_hour=resume_basic_form['per_hour'],
                    age=resume_basic_form['age'],
                )
                
                edu_form = Education(
                    profile=resume,
                    degree=resume_edu_form['degree'].title(),
                    field_of_study=resume_edu_form['field_of_study'].title(),
                    school=resume_edu_form['school'].title(),
                    start_year=resume_edu_form['start_year'],
                    end_year=resume_edu_form['end_year'],
                    description=resume_edu_form['description'].capitalize()
                )

                

                work_form = Experience(
                    profile=resume,
                    company_name=user_form_data_work['company_name'].title(),
                    title=user_form_data_work['title'].title(),
                    work_start_year=user_form_data_work['work_start_year'],
                    work_end_year=user_form_data_work['work_end_year'],
                    work_description=user_form_data_work['work_description'].capitalize()
                )
                

                # Manually create and save the Profile instance
                skill = ResumeSkill(
                    profile=resume,
                    skill_name=form.cleaned_data['skill_name'].title(),
                    proficiency=form.cleaned_data['proficiency'],
                )

                resume.save()
                work_form.save()
                edu_form.save()
                skill.save()
                
            except Exception:
                messages.error(request, form.errors)
                return render(request, 'jobseeker/resume_skill.html', {'profile':profile, 
                                                         's_form': skill_form,
                                                         'user':users})

            
            return redirect('profile')
           
        else:
            messages.error(request, form.errors)
    else:
        skill_form = SkillForm() 
    
    return render(request, 'jobseeker/resume_skill.html', {'profile':profile, 
                                                         's_form': skill_form,
                                                         'user':users})





# def add_job(request):
#     if 'user' not in request.session:
#         return redirect('index')
#
#     user = request.session['user']
#     users = CustomUser.objects.get(username=user)
#     profile = Profile.objects.get(user=users)
#
#     jobform = JobForm()
#
#     if request.method == 'POST':
#         form = JobForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             desc = form.cleaned_data['description']
#             word_count = len(desc.split())  # Count the words
#
#             if word_count < 100:
#                 error_message = f"The description must contain at least 100 words. Currently, it has {word_count} words."
#                 messages.error(request, error_message)
#                 return render(request, 'profile.html', {
#                         'form': jobform,
#                         'user': users,
#                         'profile': profile
#                 })
#             else:
#                 pass
#
#             try:
#                 new_job = Job(
#                     category=form.cleaned_data['category'].title(),
#                     title=form.cleaned_data['title'].title(),
#                     description=form.cleaned_data['description'].capitalize(),
#                     employer=users,
#                     location=form.cleaned_data['location'].title(),
#                     salary=form.cleaned_data['salary'],
#                     skills_required=form.cleaned_data['skills_required'].title(),
#                     job_tag=form.cleaned_data['job_tag'].title(),
#                     job_type=form.cleaned_data['job_type'].title(),
#                     cover_img=form.cleaned_data['cover_img']
#                 )
#
#                 new_job.save()
#
#                 return redirect('profile')
#             except Exception:
#                 messages.error(request, form.errors)
#
#         else:
#             messages.error(request, form.errors)
#
#     else:
#         form = JobForm()
#
#     return render(request, 'profile.html', {
#             'form': jobform,
#             'user': users,
#             'profile': profile
#         })
#
#

# def add_job(request):
#     if not request.user.is_authenticated:
#         return redirect('index')
#
#     user = request.user.email
#
#     # get profile information
#     user = request.user
#     try:
#         users = CustomUser.objects.get(email=user)
#         profile, created = Profile.objects.get_or_create(user=request.user)
#     except CustomUser.DoesNotExist:
#         messages.error(request, "User does not exist.")
#         return redirect('index')
#     except Profile.DoesNotExist:
#         messages.error(request, "Profile does not exist.")
#         return redirect('index')
#
#     if request.method == 'POST':
#         form = JobForm(request.POST, request.FILES)
#
#         if form.is_valid():
#             desc = form.cleaned_data['description']
#             word_count = len(desc.split())  # Count the words
#
#             if word_count < 100:
#                 error_message = f"The description must contain at least 100 words. Currently, it has {word_count} words."
#                 messages.error(request, error_message)
#             else:
#                 try:
#                     Job.objects.create(
#                         category=form.cleaned_data['category'].title(),
#                         title=form.cleaned_data['title'].title(),
#                         description=form.cleaned_data['description'].capitalize(),
#                         employer=users,
#                         location=form.cleaned_data['location'].title(),
#                         salary=form.cleaned_data['salary'],
#                         skills_required=form.cleaned_data['skills_required'].title(),
#                         job_tag=form.cleaned_data['job_tag'].title(),
#                         job_type=form.cleaned_data['job_type'].title(),
#                         cover_img=form.cleaned_data['cover_img']
#                     )
#
#                     messages.success(request, "Job added successfully!")
#                     return redirect('profile')
#                 except Exception as e:
#                     messages.error(request, f"Error saving job: {e}")
#         else:
#             messages.error(request, "Invalid form submission. Please check the entered details.")
#     else:
#         form = JobForm()
#
#     return render(request, 'profile.html', {
#         'form': form,
#         'user': users,
#         'profile': profile
#     })


def add_job(request):
    if not request.user.is_authenticated:
        return redirect('index')

    try:
        users = CustomUser.objects.get(email=request.user.email)
        profile, created = Profile.objects.get_or_create(user=request.user)
    except CustomUser.DoesNotExist:
        messages.error(request, "User does not exist.")
        return redirect('index')
    except Profile.DoesNotExist:
        messages.error(request, "Profile does not exist.")
        return redirect('index')

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)

        if form.is_valid():
            desc = form.cleaned_data['description']
            word_count = len(desc.split())

            if word_count < 100:
                messages.error(request,
                               f"The description must contain at least 100 words. Currently, it has {word_count} words.")
            else:
                try:
                    job = form.save(commit=False)  # Save form without committing to DB
                    job.employer = profile  # Assign the logged-in employer profile
                    job.category = form.cleaned_data['category'].title()
                    job.title = form.cleaned_data['title'].title()
                    job.description = form.cleaned_data['description'].capitalize()
                    job.location = form.cleaned_data['location'].title()
                    job.skills_required = form.cleaned_data['skills_required'].title()
                    job.job_tag = form.cleaned_data['job_tag'].title()
                    job.job_type = form.cleaned_data['job_type'].title()
                    job.cover_img = form.cleaned_data['cover_img']
                    job.save()  # Save to database

                    messages.success(request, "Job added successfully!")
                    return redirect('profile')
                except Exception as e:
                    messages.error(request, f"Error saving job: {e}")
        else:
            messages.error(request, "Invalid form submission. Please check the entered details.")
    else:
        form = JobForm()

    return render(request, 'profile.html', {'form': form, 'user': users, 'profile': profile})

def job_details(request,job_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    user = request.user
    users = CustomUser.objects.get(email=user)

    profile, created = Profile.objects.get_or_create(user=request.user)
    job = Job.objects.get(id=job_id)

    # random_objects = Job.objects.order_by('?')[:10]  # Fetch 10 random objects
    random_objects = Job.objects.order_by('?') # Fetch 10 random objects
    skills_list = job.skills_required.split(',') if job.skills_required else []

    return render(request, 'job_details.html', {'job': job,'skills':skills_list, 'user': users, 'profile': profile, 'random': random_objects})


def browse_jobs(request, category_name):
    # if request.user.is_authenticated:
    #     user = request.user
    #     users = CustomUser.objects.get(email=user)
    #
    #     # get profile information
    #     profile, created = Profile.objects.get_or_create(user=request.user)
    #
    #     return render(request, 'browse_jobs.html', {'user': user, 'profile': profile})
    # Convert category_name to match the JOB_CATEGORY_CHOICES keys
    category = get_object_or_404(Category, name=category_name)
    jobs = Job.objects.filter(category=category)

    context = {
            'category': category,
            'jobs': jobs
    }

    return render(request, 'browse_jobs.html', context)

    









