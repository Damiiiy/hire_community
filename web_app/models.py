from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email


class Profile(models.Model):
    """
    Extended user profile for both job seekers and employers.
    """
    USER_TYPE_CHOICES = [
        ('job_seeker', 'Job Seeker'),
        ('employer', 'Employer'),
    ]
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.user.email}"


class Activity(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="activities")
    action = models.CharField(max_length=255)  # Description of the activity
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action} at {self.timestamp}"


class Skill(models.Model):
    """
    Skills for job seekers to add to their profile or job requirements.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon_class = models.CharField(max_length=50, help_text="CSS class for icon (e.g., 'lni-home')")


class Job(models.Model):
    # JOB_CATEGORY_CHOICES = [
    #     ('technology', 'Technology'),
    #     ('design', 'Art/Design'),
    #     ('marketing', 'Sale/Marketing'),
    #     ('finance', 'Finance'),
    #     ('education', 'Education/Training'),
    #     ('healthcare', 'Healthcare'),
    #     ('science', 'Science'),
    #     ('food_services', 'Food Services')
    # ]

    JOB_TYPE_CHOICES = [
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="jobs", default=None)
    title = models.CharField(max_length=255)
    job_tag = models.CharField(max_length=255, default="General")  # Must have a default value
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    employer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255)
    salary = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    skills_required = models.CharField(max_length=255)

    job_type = models.CharField(max_length=50, choices=JOB_TYPE_CHOICES)

    cover_img = models.ImageField(upload_to='cover_images/')

    def __str__(self):
        return f"{self.title} at {self.employer.user.email}"


class Unskilled_job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    company_name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.IntegerField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    skills_required = models.CharField(max_length=255, blank=True, null=True)
    job_type = models.CharField(
        max_length=50,
        choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract')]
    )
    cover_img = models.ImageField(upload_to='cover_images/', blank=True, null=True)




class Application(models.Model):
    """
    Applications from job seekers for job postings.
    """
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True, null=True)
    resume = models.FileField(upload_to='resumes/')
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('submitted', 'Submitted'),
            ('under_review', 'Under Review'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected')
        ],
        default='submitted'
    )

    def __str__(self):
        return f"{self.applicant.user.username} - {self.job.title}"



class Message(models.Model):
    """
    Messaging between users regarding job applications or other inquiries.
    """
    sender = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_messages')
    application = models.ForeignKey(Application, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.user.username} to {self.receiver.user.username}"


class Review(models.Model):
    """
    Reviews of job seekers or employers after an application process.
    """
    reviewer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='given_reviews')
    reviewed = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='received_reviews')
    job = models.ForeignKey(Job, on_delete=models.SET_NULL, null=True, related_name='reviews')
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review from {self.reviewer.user.username} to {self.reviewed.user.username}"


class Notification(models.Model):
    """
    Notifications for job applications, messages, or reviews.
    """
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='notifications')
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)  # Link to the relevant page

    def __str__(self):
        return f"Notification for {self.user.user.username} - {'Read' if self.is_read else 'Unread'}"



########    resume data     ################################


class ResumeProfile(models.Model):
    user= models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='resume_profiles', default=None)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    profession_title = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    web = models.URLField(blank=True, null=True)
    per_hour = models.IntegerField(blank=True, null=True)
    age = models.IntegerField()

class Education(models.Model):
    profile = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    field_of_study = models.CharField(max_length=100)
    school = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    description = models.TextField(blank=True)

class Experience(models.Model):
    profile = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    work_start_year = models.IntegerField()
    work_end_year = models.IntegerField()
    work_description = models.TextField(blank=True)

class ResumeSkill(models.Model):
    profile = models.ForeignKey(ResumeProfile, on_delete=models.CASCADE, related_name='skills')
    skill_name = models.CharField(max_length=100)
    proficiency = models.IntegerField()
