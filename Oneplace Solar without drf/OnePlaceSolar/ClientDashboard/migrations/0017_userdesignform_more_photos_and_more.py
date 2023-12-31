# Generated by Django 4.0.2 on 2023-07-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ClientDashboard', '0016_alter_userdesignform_request_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdesignform',
            name='more_photos',
            field=models.ImageField(blank=True, upload_to='more_photos/'),
        ),
        migrations.AddField(
            model_name='userdesignform',
            name='site_photos',
            field=models.ImageField(blank=True, upload_to='site_photos/'),
        ),
    ]
