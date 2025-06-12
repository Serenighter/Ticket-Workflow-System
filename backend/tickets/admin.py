from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import Ticket, Department, EmployeeProfile

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['identification', 'name', 'contact_email', 'updated_at']
    list_filter = ['updated_at']
    search_fields = ['name', 'identification', 'contact_email']
    ordering = ['identification']


class EmployeeProfileInline(admin.StackedInline):
    model = EmployeeProfile
    can_delete = False
    verbose_name_plural = 'Employee Profile'
    fields = ['department']


class UserAdmin(BaseUserAdmin):
    inlines = (EmployeeProfileInline,)
    list_display = ['username', 'email', 'first_name', 'last_name', 'get_department', 'is_staff']
    list_filter = BaseUserAdmin.list_filter + ('employeeprofile__department',)
    
    def get_department(self, obj):
        try:
            return obj.employeeprofile.department
        except EmployeeProfile.DoesNotExist:
            return 'No Department'
    get_department.short_description = 'Department'
    
    def get_position(self, obj):
        try:
            return obj.employeeprofile.position
        except EmployeeProfile.DoesNotExist:
            return 'No Position'
    get_position.short_description = 'Position'


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'priority', 'category', 'created_by', 'of_department', 'assigned', 'created_at']
    list_filter = ['status', 'priority', 'category', 'of_department', 'created_at']
    search_fields = ['title', 'description', 'created_by__username', 'created_by__email']
    readonly_fields = ['created_at', 'updated_at', 'closed_at']
    ordering = ['-created_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'category')
        }),
        ('Status & Priority', {
            'fields': ('status', 'priority', 'due')
        }),
        ('Assignment', {
            'fields': ('created_by', 'of_department', 'assigned')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'closed_at'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new ticket
            if not obj.created_by:
                obj.created_by = request.user
        super().save_model(request, obj, form, change)

"""
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'priority', 'of_department', 'created_by')
    list_filter = ('status', 'priority', 'of_department')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at', 'closed_at')


admin.site.register(Department)
admin.site.register(Ticket, TicketAdmin)
"""