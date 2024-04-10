from django.contrib import admin
from .models import Post, Comment
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(User)

# Define an inline admin descriptor for Employee model
# which acts a bit like a singleton
# class EmployeeInline(admin.StackedInline):
#     model = ProfileUser
#     can_delete = False
#     verbose_name_plural = 'profileusers'
#
# # Define a new User admin
# class UserAdmin(BaseUserAdmin):
#     inlines = (EmployeeInline,)

# Re-register UserAdmin
