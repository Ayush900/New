from django.contrib import admin
from .models import ClientUsers
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class CustomsuerAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name' , 'username','is_active','is_logged_in')
    # This will display the Clientusers in the admin panel in descending order of date joined 
    # the '-' means descending
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()




admin.site.register(ClientUsers, CustomsuerAdmin)
