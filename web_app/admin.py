from django.contrib import admin

# Register your models here.
from .models import *


admin.site.register(Profile)
admin.site.register(Skill)
admin.site.register(Job)
admin.site.register(Unskilled_job)
admin.site.register(Application)
admin.site.register(Message)
admin.site.register(Review)
admin.site.register(Notification)
admin.site.register(CustomUser)

############################

admin.site.register(ResumeProfile)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(ResumeSkill)





