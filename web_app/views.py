from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.forms import modelformset_factory
from web_app.models import *
from django.contrib import messages
from django.forms import ValidationError

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
                            category=form.cleaned_data['category'],
                            title=form.cleaned_data['title'],
                            description=form.cleaned_data['description'],
                            employer=users,
                            location=form.cleaned_data['location'],
                            salary=form.cleaned_data['salary'],
                            skills_required=form.cleaned_data['skills_required'],
                            job_type=form.cleaned_data['job_type'],
                            cover_img=form.cleaned_data['cover_img']
                        )

                        # new_job.save()

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
    if 'user' in request.session:
        user = request.session['user']
        users = CustomUser.objects.get(username=user)
        profile = Profile.objects.get(user=users)
        return render(request, 'jobseeker/manage_applications.html', {'user': users, 'profile':profile} )
    

    else:
        return redirect('index')
    


    

                  
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
            
            
          
            # Manually create and save the Profile instance
            profile = Profile(
                user=user,
                user_type=form.cleaned_data['user_type'],
                bio=form.cleaned_data['bio'],
                location=form.cleaned_data['location'],
                profile_picture=form.cleaned_data['profile_picture'],
                website=form.cleaned_data['website']
            )

            i = CustomUser.objects.all()
            if user_form_data in i:
                messages.error(request, "User Exist ALready")
                return render(request, 'signup2.html', {'form': form})
            else:
                user.save()
                profile.save()
                # Log in the user and clear session data
                # login(request, user)
                request.session.pop('user_form_data', None)  # Clear session after registration
                messages.success(request, "Registration successful!")
                return render(request, 'signup2.html', {'form': form})

        else:
            messages.error(request, form.errors)
    else:
        form = ProfileForm() 
    return render(request, 'signup2.html', {'form': form})



################## RESUME DATA VIEW ##################

def resume_basic_info(request):
    if 'user' not in request.session:
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
                    name=resume_basic_form['name'],
                    email=resume_basic_form['email'],
                    profession_title=resume_basic_form['profession_title'],
                    location=resume_basic_form['location'],
                    web=resume_basic_form['web'],
                    per_hour=resume_basic_form['per_hour'],
                    age=resume_basic_form['age'],
                )
                
                edu_form = Education(
                    profile=resume,
                    degree=resume_edu_form['degree'],
                    field_of_study=resume_edu_form['field_of_study'],
                    school=resume_edu_form['school'],
                    start_year=resume_edu_form['start_year'],
                    end_year=resume_edu_form['end_year'],
                    description=resume_edu_form['description']
                )

                

                work_form = Experience(
                    profile=resume,
                    company_name=user_form_data_work['company_name'],
                    title=user_form_data_work['title'],
                    work_start_year=user_form_data_work['work_start_year'],
                    work_end_year=user_form_data_work['work_end_year'],
                    work_description=user_form_data_work['work_description']
                )
                

                # Manually create and save the Profile instance
                skill = ResumeSkill(
                    profile=resume,
                    skill_name=form.cleaned_data['skill_name'],
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





def add_job(request):
    if 'user' not in request.session:
        return redirect('index')
    
    user = request.session['user']
    users = CustomUser.objects.get(username=user)
    profile = Profile.objects.get(user=users)

    jobform = JobForm()

    if request.method == 'POST':
        form = JobForm(request.POST, request.FILES)

        if form.is_valid():
            desc = form.cleaned_data['description']
            word_count = len(desc.split())  # Count the words

            if word_count < 100:
                error_message = f"The description must contain at least 100 words. Currently, it has {word_count} words."
                messages.error(request, error_message)
                return render(request, 'profile.html', {
                        'form': jobform,
                        'user': users,
                        'profile': profile
                })    
            else:
                pass                

            try:
                new_job = Job(
                    category=form.cleaned_data['category'],
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    employer=users,
                    location=form.cleaned_data['location'],
                    salary=form.cleaned_data['salary'],
                    skills_required=form.cleaned_data['skills_required'],
                    job_type=form.cleaned_data['job_type'],
                    cover_img=form.cleaned_data['cover_img']
                )

                new_job.save()

                return redirect('profile')
            except Exception:
                messages.error(request, form.errors)

        else:
            messages.error(request, form.errors)

    else:
        form = JobForm()

    return render(request, 'profile.html', {
            'form': jobform,
            'user': users,
            'profile': profile
        })                    



def job_details(request,job_id):
    if 'user' not in request.session:
        return redirect('index')
    
    user = request.session['user']
    users = CustomUser.objects.get(username=user)
    profile = Profile.objects.get(user=users)

    job = Job.objects.get(id=job_id)

    # random_objects = Job.objects.order_by('?')[:10]  # Fetch 10 random objects
    random_objects = Job.objects.order_by('?') # Fetch 10 random objects



    skills_list = job.skills_required.split(',') if job.skills_required else []


    return render(request, 'job_details.html', {'job': job,'skills':skills_list, 'user': users, 'profile': profile, 'random': random_objects})

    

    

    









