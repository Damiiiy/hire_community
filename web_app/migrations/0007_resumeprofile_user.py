# Generated by Django 5.1.2 on 2024-11-10 12:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0006_rename_description_experience_work_description_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumeprofile',
            name='user',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='resume_profiles', to='web_app.customuser'),
        ),
    ]