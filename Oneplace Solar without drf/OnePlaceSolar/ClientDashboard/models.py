from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver

from rest_framework_simplejwt.tokens import OutstandingToken
from multiselectfield import MultiSelectField


# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, email, password=None, phone_number='', user_type='homeowner', company_name=''):
        if not email:
            raise ValueError('Email should be provided')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone_number=phone_number,
            user_type=user_type,
            company_name=company_name
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class ClientUsers(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('homeowner', 'Homeowner'),
        ('contractor', 'Contractor'),
    )
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='homeowner')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=10, blank=True)
    user_type = models.CharField(
        max_length=20, choices=USER_TYPE_CHOICES, default='homeowner')
    company_name = models.CharField(max_length=100, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)
    is_logged_in = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()

    def __str__(self):
        return self.email

    # def has_perm(self, perm, obj=None):
    #     # Check if the user has the permission to view or change client users
    #     if perm == "ClientDashboard.view_clientusers" or perm == "ClientDashboard.change_clientusers":
    #         return True
    #     return False

    def has_module_perms(self, app_label: str):
        # Restrict access to the app_name app
        # if app_label == 'app_name':
        #     return True
        # return False
        return True


class UserDesignForm(models.Model):
    REQUEST_TYPE_CHOICES = (
        ('solar_preliminary_design', 'Solar Preliminary Design'),
        ('solar_permit_plan', 'Solar Permit Plan'),
        ('engineering_stamp', 'Engineering Stamp'),
        ('interconnection_and_permitting_service',
         'Interconnection and Permitting Service'),
    )
    JOB_TYPE_CHOICES = (
        ('pv', 'PV'),
        ('pv_storage', 'PV + Storage'),
        ('storage', 'Storage Only'),
        ('pv_storage_generator', 'PV + Storage + Generator'),
    )
    PROPERTY_TYPE_COICES = (
        ('residential', 'Residential'),
        ('commercial', 'Commercial')
    )
    CONSTRUCTION_TYPE_COICES = (
        ('old', 'Old'),
        ('new', 'New')
    )
    MOUNTING_TYPE_COICES = (
        ('roof', 'Roof'),
        ('ground', 'Ground'),
        ('carport', 'Carport')
    )
    FRAMING_TYPE_CHOICES = (
        ('rafter', 'Rafter'),
        ('truss', 'Truss')
    )
    BATTERY_BACKUP_CHOICES = (
        ('partial_home', 'Partial Home'),
        ('whole_home', 'Whole Home')
    )
    STAMPING_CHOICES = (
        ('structural', 'Structural'),
        ('electrical', 'Electrical'),
        ('both', 'Both'),
        ('not_required', 'Not Required')
    )
    APPLICATION_REQUEST_CHOICES = (
        ('permitting_application', 'Permitting Application'),
        ('interconnection_application', 'Interconnection Application'),
        ('both', 'Both'),
        ('not_required', 'Not Required')
    )
    job_address = models.CharField(max_length=255, unique=True)
    request_type = MultiSelectField(
        choices=REQUEST_TYPE_CHOICES, blank=True, null=True)

    client = models.ForeignKey(ClientUsers, on_delete=models.CASCADE)
    ahj_name = models.CharField(max_length=50, blank=True, null=True)
    job_type = models.CharField(
        max_length=50, choices=JOB_TYPE_CHOICES, blank=True, null=True)
    property_type = models.CharField(
        max_length=50, choices=PROPERTY_TYPE_COICES, blank=True, null=True)
    construction = models.CharField(
        max_length=50, choices=CONSTRUCTION_TYPE_COICES, blank=True, null=True)
    mounting = models.CharField(
        max_length=50, choices=MOUNTING_TYPE_COICES, blank=True, null=True)
    framing_type = models.CharField(
        max_length=50, choices=FRAMING_TYPE_CHOICES, blank=True, null=True)
    framing_size_capacity = models.CharField(
        max_length=50, blank=True, null=True)
    module_model_name = models.CharField(max_length=50, blank=True, null=True)
    module_count = models.IntegerField(blank=True, null=True)
    battery_backup = models.CharField(
        max_length=50, choices=BATTERY_BACKUP_CHOICES, blank=True, null=True)
    main_service_panel_rating = models.CharField(
        max_length=50, blank=True, null=True)
    point_of_interconnection = models.CharField(
        max_length=50, blank=True, null=True)
    contractor_logo = models.ImageField(
        upload_to='contractor_logo/', blank=True)
    site_photos = models.ImageField(upload_to='site_photos/', blank=True)
    more_photos = models.ImageField(upload_to='more_photos/', blank=True)
    google_drive_link = models.CharField(max_length=255, blank=True, null=True)
    stamping = models.CharField(
        max_length=50, choices=STAMPING_CHOICES, default='not_required')
    application_request = models.CharField(
        max_length=50, choices=APPLICATION_REQUEST_CHOICES, default='not_required')
    instructions_comments = models.CharField(
        max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.client.first_name} {self.client.last_name}'s DesignForm"
