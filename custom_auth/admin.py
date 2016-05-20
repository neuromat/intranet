from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext_lazy as _
from custom_auth.models import User
from custom_auth.forms import UserChangeForm, UserCreationForm


class CustomUserAdmin(UserAdmin):
    """
    Only Superuser can see fildsets. Common user uses restricted_fieldsets.
    To create a new user, add_fieldsets is used. Don't worry, UserAdmin knows add_fieldsets.
    """
    form = UserChangeForm
    add_form = UserCreationForm

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Permissions'), {'fields': ('is_staff', 'is_active', 'is_nira_admin', 'is_superuser', 'user_profile',
                                       'user_permissions', 'groups')}),
    )

    restricted_fieldsets = (
        (None, {'fields': ('username', 'password')}),
    )

    add_fieldsets = (
        (None, {'fields': ('username', 'password1', 'password2')}),
    )

    list_display = ('username', 'is_staff')
    ordering = ('username',)

    # Shows users according to the user permission
    def get_queryset(self, request):
        if request.user.is_superuser:
            return User.objects.all()
        return User.objects.filter(username=request.user)

    # For updates, if not superuser, show restricted_fieldsets.
    def get_fieldsets(self, request, obj=None):
        if request.user.is_superuser:
            return super(CustomUserAdmin, self).get_fieldsets(request, obj)
        return self.restricted_fieldsets

admin.site.register(User, CustomUserAdmin)
