from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from .models import User, Recipe


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    # This is the field that is used to order the users
    list_display = ['email',
                    'name']
    # This is the list of fields that are displayed in the admin page
    fieldsets = (
        # This is the form that is displayed when creating a new user
        (None, {'fields': ('email', 'password')}),
        (_('Permissions'),
         {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        (_('Important Dates'), {'fields': ('last_login',)})
    )
    readonly_fields = ['last_login']
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            # This is the class that is used to style the form
            'fields': (
                # This is the list of fields that are displayed in the admin
                # page when creating a new user
                'email',
                'password1',
                'password2',
                'name',
                'is_active',
                'is_staff',
                'is_superuser')
        }),
    )


admin.site.register(User, UserAdmin)
admin.site.register(Recipe)
