from django.contrib import admin
from .models import Employee, Attendance


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """Admin configuration for Employee model"""
    
    list_display = ['employee_id', 'full_name', 'email', 'department', 'created_at']
    list_filter = ['department', 'created_at']
    search_fields = ['employee_id', 'full_name', 'email', 'department']
    ordering = ['employee_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Employee Information', {
            'fields': ('employee_id', 'full_name', 'email', 'department')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    """Admin configuration for Attendance model"""
    
    list_display = ['employee', 'date', 'status', 'created_at']
    list_filter = ['status', 'date', 'employee__department']
    search_fields = ['employee__employee_id', 'employee__full_name']
    ordering = ['-date', 'employee__employee_id']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        ('Attendance Information', {
            'fields': ('employee', 'date', 'status')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """Optimize queryset with select_related"""
        return super().get_queryset(request).select_related('employee')
