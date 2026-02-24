from rest_framework import serializers
from .models import Employee, Attendance
from django.core.exceptions import ValidationError as DjangoValidationError


class EmployeeSerializer(serializers.ModelSerializer):
    """Serializer for Employee model"""
    
    class Meta:
        model = Employee
        fields = ['id', 'employee_id', 'full_name', 'email', 'department', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_employee_id(self, value):
        """Validate employee_id format"""
        if not value.isalnum():
            raise serializers.ValidationError(
                "Employee ID must contain only letters and numbers."
            )
        return value

    def validate_full_name(self, value):
        """Validate full_name format"""
        if any(char.isdigit() for char in value):
            raise serializers.ValidationError(
                "Full name cannot contain numbers."
            )
        return value.strip()

    def validate_email(self, value):
        """Validate email format and uniqueness"""
        if self.instance and self.instance.email == value:
            return value
        
        if Employee.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "An employee with this email already exists."
            )
        return value.lower()

    def validate(self, attrs):
        """Cross-field validation"""
        # Check for duplicate employee_id during creation or update
        employee_id = attrs.get('employee_id')
        if employee_id:
            existing_employee = Employee.objects.filter(employee_id=employee_id)
            if self.instance:
                existing_employee = existing_employee.exclude(pk=self.instance.pk)
            
            if existing_employee.exists():
                raise serializers.ValidationError({
                    'employee_id': 'An employee with this ID already exists.'
                })
        
        return attrs


class AttendanceSerializer(serializers.ModelSerializer):
    """Serializer for Attendance model"""
    
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'employee', 'employee_id', 'employee_name', 
            'date', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_date(self, value):
        """Validate attendance date"""
        from django.utils import timezone
        
        if value > timezone.now().date():
            raise serializers.ValidationError(
                "Attendance date cannot be in the future."
            )
        return value

    def validate(self, attrs):
        """Cross-field validation"""
        employee = attrs.get('employee')
        date = attrs.get('date')
        
        if employee and date:
            # Check for duplicate attendance record
            existing_attendance = Attendance.objects.filter(
                employee=employee, 
                date=date
            )
            
            if self.instance:
                existing_attendance = existing_attendance.exclude(pk=self.instance.pk)
            
            if existing_attendance.exists():
                raise serializers.ValidationError({
                    'non_field_errors': [
                        f"Attendance record for {employee.full_name} on {date} already exists."
                    ]
                })
        
        return attrs


class AttendanceListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing attendance records"""
    
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    employee_id = serializers.CharField(source='employee.employee_id', read_only=True)
    department = serializers.CharField(source='employee.department', read_only=True)
    
    class Meta:
        model = Attendance
        fields = [
            'id', 'employee_id', 'employee_name', 'department',
            'date', 'status', 'created_at'
        ]


class EmployeeAttendanceSummarySerializer(serializers.ModelSerializer):
    """Serializer for employee with attendance summary"""
    
    total_present_days = serializers.SerializerMethodField()
    total_absent_days = serializers.SerializerMethodField()
    total_records = serializers.SerializerMethodField()
    
    class Meta:
        model = Employee
        fields = [
            'id', 'employee_id', 'full_name', 'email', 'department',
            'total_present_days', 'total_absent_days', 'total_records'
        ]

    def get_total_present_days(self, obj):
        """Get total present days for the employee"""
        return obj.attendance_records.filter(status='Present').count()

    def get_total_absent_days(self, obj):
        """Get total absent days for the employee"""
        return obj.attendance_records.filter(status='Absent').count()

    def get_total_records(self, obj):
        """Get total attendance records for the employee"""
        return obj.attendance_records.count()
