from django.contrib import admin
# Register your models here.
from .models import CustomUser
# Register your models here.
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'last_name','is_staff','first_name', 'email', 'is_superuser','date_joined')
    search_fields = ('last_name', 'email', 'username','first_name')
    fields = ('name', 'email', 'username','password','status','is_staff','is_superuser')
    

admin.site.register(CustomUser, CustomUserAdmin)
