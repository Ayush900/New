# Generated by Django 4.0.2 on 2023-07-16 12:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ClientDashboard', '0014_alter_clientusers_is_superuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDesignForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_address', models.CharField(max_length=50, unique=True)),
                ('request_type', models.CharField(blank=True, choices=[('solar_preliminary_design', 'Solar Preliminary Design'), ('solar_permit_plan', 'Solar Permit Plan'), ('engineering_stamp', 'Engineering Stamp'), ('interconnection_and_permitting_service', 'Interconnection and Permitting Service')], max_length=50, null=True)),
                ('ahj_name', models.CharField(blank=True, max_length=50, null=True)),
                ('job_type', models.CharField(blank=True, choices=[('pv', 'PV'), ('pv_storage', 'PV + Storage'), ('storage', 'Storage Only'), ('pv_storage_generator', 'PV + Storage + Generator')], max_length=50, null=True)),
                ('property_type', models.CharField(blank=True, choices=[('residential', 'Residential'), ('commercial', 'Commercial')], max_length=50, null=True)),
                ('construction', models.CharField(blank=True, choices=[('old', 'Old'), ('new', 'New')], max_length=50, null=True)),
                ('mounting', models.CharField(blank=True, choices=[('roof', 'Roof'), ('ground', 'Ground'), ('carport', 'Carport')], max_length=50, null=True)),
                ('framing_type', models.CharField(blank=True, choices=[('rafter', 'Rafter'), ('truss', 'Truss')], max_length=50, null=True)),
                ('framing_size_capacity', models.CharField(blank=True, max_length=50, null=True)),
                ('module_model_name', models.CharField(blank=True, max_length=50, null=True)),
                ('module_count', models.IntegerField(blank=True, null=True)),
                ('battery_backup', models.CharField(blank=True, choices=[('partial_home', 'Partial Home'), ('whole_home', 'Whole Home')], max_length=50, null=True)),
                ('main_service_panel_rating', models.CharField(blank=True, max_length=50, null=True)),
                ('point_of_interconnection', models.CharField(blank=True, max_length=50, null=True)),
                ('contractor_logo', models.ImageField(blank=True, upload_to='contractor_logo/')),
                ('google_drive_link', models.CharField(blank=True, max_length=255, null=True)),
                ('stamping', models.CharField(choices=[('structural', 'Structural'), ('electrical', 'Electrical'), ('both', 'Both'), ('not_required', 'Not Required')], default='not_required', max_length=50)),
                ('application_request', models.CharField(choices=[('permitting_application', 'Permitting Application'), ('interconnection_application', 'Interconnection Application'), ('both', 'Both'), ('not_required', 'Not Required')], default='not_required', max_length=50)),
                ('instructions_comments', models.CharField(blank=True, max_length=255, null=True)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
