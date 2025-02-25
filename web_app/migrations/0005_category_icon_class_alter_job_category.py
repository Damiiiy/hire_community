# Generated by Django 5.1.2 on 2025-02-24 10:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0004_alter_job_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='icon_class',
            field=models.CharField(default=None, help_text="CSS class for icon (e.g., 'lni-home')", max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='category',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='web_app.category'),
        ),
    ]
