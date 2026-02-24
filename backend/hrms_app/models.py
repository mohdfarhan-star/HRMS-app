from django.db import models
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError


class Employee(models.Model):
    """Employee model for storing employee information"""
    
    employee_id = models.CharField(
        max_length=20, 
        unique=True, 
        help_text="Unique employee identifier"
    )
    full_name = models.CharField(
        max_length=100, 
        help_text="Employee's full name"
    )
    email = models.EmailField(
        unique=True,
        validators=[EmailValidator()],
        help_text="Employee's email address"
    )
    department = models.CharField(
        max_length=50,
        help_text="Employee's department"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['employee_id']
        verbose_name = 'Employee'
        verbose_name_plural = 'Employees'

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"

    def clean(self):
        """Custom validation for the Employee model"""
        super().clean()
        
        # Validate employee_id format (alphanumeric)
        if not self.employee_id.isalnum():
            raise ValidationError({
                'employee_id': 'Employee ID must contain only letters and numbers.'
            })
        
        # Validate full_name (no numbers)
        if any(char.isdigit() for char in self.full_name):
            raise ValidationError({
                'full_name': 'Full name cannot contain numbers.'
            })


class Attendance(models.Model):
    """Attendance model for tracking employee attendance"""
    
    ATTENDANCE_STATUS_CHOICES = [
        ('Present', 'Present'),
        ('Absent', 'Absent'),
    ]
    
    employee = models.ForeignKey(
        Employee, 
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    date = models.DateField(help_text="Attendance date")
    status = models.CharField(
        max_length=10,
        choices=ATTENDANCE_STATUS_CHOICES,
        help_text="Attendance status"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-date', 'employee__employee_id']
        unique_together = ['employee', 'date']
        verbose_name = 'Attendance Record'
        verbose_name_plural = 'Attendance Records'

    def __str__(self):
        return f"{self.employee.employee_id} - {self.date} - {self.status}"

    def clean(self):
        """Custom validation for the Attendance model"""
        super().clean()
        
        # Ensure date is not in the future
        from django.utils import timezone
        if self.date and self.date > timezone.now().date():
            raise ValidationError({
                'date': 'Attendance date cannot be in the future.'
            })
