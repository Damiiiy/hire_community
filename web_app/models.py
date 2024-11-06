from django.db import models




class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Storing as a hash

    def __str__(self):
        return self.username

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
        return f"{self.user.username} - {self.get_user_type_display()}"


class Skill(models.Model):
    """
    Skills for job seekers to add to their profile or job requirements.
    """
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Job(models.Model):
    """
    Job postings created by employers.
    """
    title = models.CharField(max_length=255)
    description = models.TextField()
    employer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='jobs')
    location = models.CharField(max_length=255, blank=True, null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_remote = models.BooleanField(default=False)
    skills_required = models.ManyToManyField(Skill, blank=True)
    job_type = models.CharField(
        max_length=50,
        choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract')]
    )

    def __str__(self):
        return f"{self.title} at {self.employer.user.username}"


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





# class job_categories(models.Model):
#     name = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self) -> str:
#         return self.name

# class Creator_user(models.Model):
#     first_name = models.CharField(max_length=255, blank=True, null=True)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     username = models.CharField(max_length=255, blank=True, null=True, unique=True)
#     password = models.CharField(max_length=255, blank=True, null=True)

#     def __str__(self) -> str:
#         return self.username

# class Jobs(models.Model):
#     title = models.CharField(max_length=255, blank=True, null=True)
#     description = models.CharField(max_length=255, blank=True, null=True)
#     applicatants = models.ForeignKey(Creator_user, on_delete=models.CASCADE)
    
#     pay_ammount = models.IntegerField(null=True, blank=True)
#     date = models.DateField(null=True, blank=True, default=timezone.now)





# class Normal_user(models.Model):
#     first_name = models.CharField(max_length=255, blank=True, null=True)
#     last_name = models.CharField(max_length=255, blank=True, null=True)
#     username = models.CharField(max_length=255, blank=True, null=True, unique=True)
#     password = models.CharField(max_length=255, blank=True, null=True)
