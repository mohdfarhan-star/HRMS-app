from django.urls import path
from . import views

urlpatterns = [
    # Employee URLs
    path('employees/', views.EmployeeListCreateView.as_view(), name='employee-list-create'),
    path('employees/<int:pk>/', views.EmployeeDetailView.as_view(), name='employee-detail'),
    path('employees/simple/', views.employee_list_simple, name='employee-list-simple'),
    path('employees/<int:employee_id>/attendance-summary/', views.employee_attendance_summary, name='employee-attendance-summary'),
    
    # Attendance URLs
    path('attendance/', views.AttendanceListCreateView.as_view(), name='attendance-list-create'),
    path('attendance/<int:pk>/', views.AttendanceDetailView.as_view(), name='attendance-detail'),
    
    # Dashboard URLs
    path('dashboard/', views.dashboard_summary, name='dashboard-summary'),
]
