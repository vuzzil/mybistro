from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from accounts.models import BistroUser
from .forms import UserCreationForm, UserChangeForm

# class BistroUserAdmin(admin.ModelAdmin):
#     model = BistroUser


User = get_user_model()

# Remove Group Model from admin. We're not using it.
admin.site.unregister(Group)


class BistroUserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'username', 'is_staff', 'is_admin')
    list_filter = ('is_staff','is_admin')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'theme')}),
        ('Permissions', {'fields': ('is_staff','is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'theme', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Register accounts Models
admin.site.register(BistroUser, BistroUserAdmin)
