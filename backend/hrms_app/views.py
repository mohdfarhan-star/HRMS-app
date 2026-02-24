from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.utils import timezone
from datetime import datetime
from .models import Employee, Attendance
from .serializers import (
    EmployeeSerializer, 
    AttendanceSerializer, 
    AttendanceListSerializer,
    EmployeeAttendanceSummarySerializer
)


class EmployeeListCreateView(generics.ListCreateAPIView):
    """
    List all employees or create a new employee
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def get_queryset(self):
        """
        Optionally filter employees by department or search term
        """
        queryset = Employee.objects.all()
        department = self.request.query_params.get('department', None)
        search = self.request.query_params.get('search', None)
        
        if department:
            queryset = queryset.filter(department__icontains=department)
        
        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search) |
                Q(employee_id__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset

    def create(self, request, *args, **kwargs):
        """
        Create a new employee with proper error handling
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'message': 'Employee created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {
                'message': 'Failed to create employee',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class EmployeeDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an employee
    """
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer

    def update(self, request, *args, **kwargs):
        """
        Update an employee with proper error handling
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    'message': 'Employee updated successfully',
                    'data': serializer.data
                }
            )
        return Response(
            {
                'message': 'Failed to update employee',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete an employee with proper response
        """
        instance = self.get_object()
        employee_name = instance.full_name
        self.perform_destroy(instance)
        return Response(
            {
                'message': f'Employee {employee_name} deleted successfully'
            },
            status=status.HTTP_200_OK
        )


class AttendanceListCreateView(generics.ListCreateAPIView):
    """
    List all attendance records or create a new attendance record
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def get_queryset(self):
        """
        Filter attendance records by employee, date range, or status
        """
        queryset = Attendance.objects.select_related('employee').all()
        
        employee_id = self.request.query_params.get('employee_id', None)
        employee = self.request.query_params.get('employee', None)
        date_from = self.request.query_params.get('date_from', None)
        date_to = self.request.query_params.get('date_to', None)
        status_filter = self.request.query_params.get('status', None)
        
        if employee_id:
            queryset = queryset.filter(employee__employee_id=employee_id)
        
        if employee:
            queryset = queryset.filter(employee__id=employee)
        
        if date_from:
            try:
                date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
                queryset = queryset.filter(date__gte=date_from)
            except ValueError:
                pass
        
        if date_to:
            try:
                date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
                queryset = queryset.filter(date__lte=date_to)
            except ValueError:
                pass
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        return queryset

    def get_serializer_class(self):
        """
        Use different serializers for list and create operations
        """
        if self.request.method == 'GET':
            return AttendanceListSerializer
        return AttendanceSerializer

    def create(self, request, *args, **kwargs):
        """
        Create a new attendance record with proper error handling
        """
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(
                {
                    'message': 'Attendance record created successfully',
                    'data': serializer.data
                },
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        return Response(
            {
                'message': 'Failed to create attendance record',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class AttendanceDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Retrieve, update or delete an attendance record
    """
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializer

    def update(self, request, *args, **kwargs):
        """
        Update an attendance record with proper error handling
        """
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        
        if serializer.is_valid():
            self.perform_update(serializer)
            return Response(
                {
                    'message': 'Attendance record updated successfully',
                    'data': serializer.data
                }
            )
        return Response(
            {
                'message': 'Failed to update attendance record',
                'errors': serializer.errors
            },
            status=status.HTTP_400_BAD_REQUEST
        )

    def destroy(self, request, *args, **kwargs):
        """
        Delete an attendance record with proper response
        """
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {
                'message': 'Attendance record deleted successfully'
            },
            status=status.HTTP_200_OK
        )


@api_view(['GET'])
def employee_attendance_summary(request, employee_id):
    """
    Get attendance summary for a specific employee
    """
    try:
        employee = Employee.objects.get(id=employee_id)
        serializer = EmployeeAttendanceSummarySerializer(employee)
        return Response(
            {
                'message': 'Employee attendance summary retrieved successfully',
                'data': serializer.data
            }
        )
    except Employee.DoesNotExist:
        return Response(
            {
                'message': 'Employee not found'
            },
            status=status.HTTP_404_NOT_FOUND
        )


@api_view(['GET'])
def dashboard_summary(request):
    """
    Get dashboard summary with counts and statistics
    """
    total_employees = Employee.objects.count()
    total_attendance_records = Attendance.objects.count()
    
    # Today's attendance
    today = timezone.now().date()
    today_present = Attendance.objects.filter(date=today, status='Present').count()
    today_absent = Attendance.objects.filter(date=today, status='Absent').count()
    
    # Recent attendance records
    recent_attendance = Attendance.objects.select_related('employee').order_by('-date', '-created_at')[:10]
    recent_attendance_data = AttendanceListSerializer(recent_attendance, many=True).data
    
    # Department-wise employee count
    from django.db.models import Count
    department_stats = Employee.objects.values('department').annotate(
        count=Count('id')
    ).order_by('-count')
    
    return Response(
        {
            'message': 'Dashboard summary retrieved successfully',
            'data': {
                'total_employees': total_employees,
                'total_attendance_records': total_attendance_records,
                'today_attendance': {
                    'present': today_present,
                    'absent': today_absent,
                    'total': today_present + today_absent
                },
                'recent_attendance': recent_attendance_data,
                'department_stats': list(department_stats)
            }
        }
    )


@api_view(['GET'])
def employee_list_simple(request):
    """
    Get a simple list of employees for dropdown/selection purposes
    """
    employees = Employee.objects.all().values('id', 'employee_id', 'full_name', 'department')
    return Response(
        {
            'message': 'Employee list retrieved successfully',
            'data': list(employees)
        }
    )
