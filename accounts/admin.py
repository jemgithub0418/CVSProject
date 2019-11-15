from django.contrib import admin
from django.contrib.auth.models import Group, Permission
from django.contrib.admin.models import LogEntry
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm
from .models import User, StaffProfile, StudentProfile
# from student_dashboard.models import


class StaffProfileInline(admin.StackedInline):
    model = StaffProfile
    verbose_name_plural = 'Staff Profile'
    verbose_name = 'User'
    fk_name = 'user'


# class StudentProfileInline(admin.StackedInline):
#     model = StudentProfile
#     verbose_name_plural = 'Student Profile'
#     verbose_name = 'Student'
#     fk_name = 'user'


def make_inactive(modeladmin, request, queryset):
    queryset.update(is_active=False)


make_inactive.short_description = 'Mark selected users as inactive.'


def make_active(modeladmin, request, queryset):
    queryset.update(is_active=True)


make_active.short_description = 'Mark selected users as active.'


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm

    actions = None
    list_editable = ['is_active', ]

    #prepopulated_fields = {'username': ('first_name', 'last_name', )}

    add_fieldsets = (
        ('Personal Info', {
            'description': '',
            'classes': ('wide',),
            'fields': ('first_name', 'middle_name', 'last_name', 'email', 'username', 'password1', 'password2', ),
        }),
        # ('User Type', {'fields': ('user_level',)}),
        ('User Type', {'fields': ('is_active', 'is_registrar',
                                  'is_teacher', 'is_superuser', 'is_student',)}),
    )

    list_display = ('last_name', 'first_name',
                    'username', 'email', 'is_active',)
    list_display_links = ('last_name', 'first_name',
                          'username', 'email',)
    list_filter = ('user_level', 'is_active')  # removed is_student here

    fieldsets = (
        ('Personal Info', {'fields': ('username', 'first_name',
                                      'middle_name', 'last_name', 'email', 'password',)}),
        ('User Type', {'fields': ('is_active', 'is_registrar',
                                  'is_teacher', 'is_superuser', 'is_student',)}),
    )
    search_fields = ('first_name', 'last_name', 'username',
                     'email', 'user_studentprofile__section__section',)
    ordering = ('last_name', 'first_name')
    filter_horizontal = ()

    def has_delete_permission(self, request, obj=None):
        return False
# source code: https://stackoverflow.com/questions/1618728/disable-link-to-edit-object-in-djangos-admin-display-list-only


class StudentProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['user']
    list_display = ('user', 'lrn', 'year', 'section', 'class_advisor')
    list_display_links = ('user', 'lrn', 'year', 'section', 'class_advisor')

    fieldsets = (
        ('Student Information', {'fields': ('user', 'lrn', 'year', 'section',
                                            'class_advisor', 'address', 'landline_number', 'mobile_number',)}),
        ('Other Information', {'fields': ('fathers_name', 'mothers_name',
                                          'contact_person_name', 'contact_person_number', )}),
    )

    def has_delete_permission(self, request, obj=None):
        return False


class StaffProfileAdmin(admin.ModelAdmin):
    actions = None
    readonly_fields = ['user']
    search_fields = ['user__username', 'user__last_name',
                     'user__first_name', 'employee_number', ]
    list_filter = ('user__user_level',)
    list_display = (
        'user', 'employee_number', 'mobile_number', 'address',
    )
    list_display_links = (
        'user', 'employee_number', 'mobile_number', 'address',
    )
    fieldsets = (
        ('Personal Info', {'fields': ('user', 'employee_number', 'mobile_number', 'address')}),
    )
    add_fieldsets = (
        ('Personal Info', {'fields': ('employee_number', 'mobile_number', 'address')}),
    )

    def has_delete_permission(self, request, obj=None):
        return False


class LogEntryAdmin(admin.ModelAdmin):
    actions = None
    list_display = (
        'user', 'content_type', 'object_id', 'object_repr',
        'action_flag', 'get_change_message', 'action_time',
    )
    list_filter = ('action_flag', 'action_time')
    search_fields = ['=user__first_name', '=user__last_name', '=user__username', ]
    fieldsets = [
        (None, {'fields': ()}),
    ]
    # change_message.short_description = 'Actions done'

    def __init__(self, *args, **kwargs):
        super(LogEntryAdmin, self).__init__(*args, **kwargs)
        self.list_display_links = None
        # removes link on objects

    def has_add_permission(self, request):
        return False
        # removes add action

    def has_delete_permission(self, request, obj=None):
        return False
    #     # removes delete action

    def has_change_permission(self, request, obj=None):
        return False
        # removes edit action


admin.site.site_header = 'CVS Administration Site'
admin.site.site_title = 'CVS Admin Portal'
admin.site.index_title = 'CVS Admin Home'
admin.site.register(User, UserAdmin)
admin.site.register(StaffProfile, StaffProfileAdmin)
admin.site.unregister(Group)
admin.site.register(LogEntry, LogEntryAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
