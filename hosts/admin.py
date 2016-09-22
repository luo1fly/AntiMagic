from django.contrib import admin
from django.contrib.auth.models import Group
from django import forms
from hosts import models
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = models.UserProfile
        fields = ('email', 'token')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField(label="Password",
        help_text=("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = models.UserProfile
        fields = ('email', 'password','is_active', 'is_admin')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserProfileAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin', 'is_active', 'id')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'department', 'tel', 'mobile', 'memo')}),
        ('API TOKEN info', {'fields': ('token',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin')}),
        ('账户有效期', {'fields': ('valid_begin_time', 'valid_end_time')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (
            None, {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2', 'is_active', 'is_admin'),
            },
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


class HostAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address', 'idc', 'port', 'enabled', 'memo')
    search_fields = ('name', 'ip_address', 'idc__name', 'port', 'enabled', 'memo')
    # 注意关联字段的搜索方式idc__name
    list_filter = ('idc', 'enabled')
    # list_editable = ('enabled',)


class HostUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'auth_type', 'password')


class BindHostToUserAdmin(admin.ModelAdmin):
    list_display = ('host', 'host_user', 'get_groups')
    filter_horizontal = ('host_groups',)


admin.site.unregister(Group)
# admin不显示分组
admin.site.register(models.UserProfile, UserProfileAdmin)
admin.site.register(models.Host, HostAdmin)
admin.site.register(models.IDC)
admin.site.register(models.HostUser, HostUserAdmin)
admin.site.register(models.HostGroup)
admin.site.register(models.BindHostToUser, BindHostToUserAdmin)
admin.site.register(models.TaskLog)
admin.site.register(models.TaskLogDetail)