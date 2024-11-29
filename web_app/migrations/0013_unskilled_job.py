# Generated by Django 5.1.2 on 2024-11-28 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0012_job_cover_img'),
    ]

    operations = [
        migrations.CreateModel(
            name='Unskilled_job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('company_name', models.CharField(max_length=255)),
                ('location', models.CharField(blank=True, max_length=255, null=True)),
                ('salary', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateField(auto_now_add=True)),
                ('skills_required', models.CharField(blank=True, max_length=255, null=True)),
                ('job_type', models.CharField(choices=[('full_time', 'Full Time'), ('part_time', 'Part Time'), ('contract', 'Contract')], max_length=50)),
                ('cover_img', models.ImageField(blank=True, null=True, upload_to='cover_images/')),
            ],
        ),
    ]
