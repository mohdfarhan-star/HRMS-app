from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Employee, Attendance
from datetime import date


class EmployeeModelTest(TestCase):
    """Test cases for Employee model"""
    
    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id="EMP001",
            full_name="John Doe",
            email="john.doe@example.com",
            department="IT"
        )
    
    def test_employee_creation(self):
        """Test employee creation"""
        self.assertEqual(self.employee.employee_id, "EMP001")
        self.assertEqual(self.employee.full_name, "John Doe")
        self.assertEqual(self.employee.email, "john.doe@example.com")
        self.assertEqual(self.employee.department, "IT")
    
    def test_employee_str_representation(self):
        """Test employee string representation"""
        expected = "EMP001 - John Doe"
        self.assertEqual(str(self.employee), expected)


class AttendanceModelTest(TestCase):
    """Test cases for Attendance model"""
    
    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id="EMP001",
            full_name="John Doe",
            email="john.doe@example.com",
            department="IT"
        )
        self.attendance = Attendance.objects.create(
            employee=self.employee,
            date=date.today(),
            status="Present"
        )
    
    def test_attendance_creation(self):
        """Test attendance creation"""
        self.assertEqual(self.attendance.employee, self.employee)
        self.assertEqual(self.attendance.date, date.today())
        self.assertEqual(self.attendance.status, "Present")
    
    def test_attendance_str_representation(self):
        """Test attendance string representation"""
        expected = f"EMP001 - {date.today()} - Present"
        self.assertEqual(str(self.attendance), expected)


class EmployeeAPITest(APITestCase):
    """Test cases for Employee API endpoints"""
    
    def setUp(self):
        self.employee_data = {
            "employee_id": "EMP001",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "department": "IT"
        }
    
    def test_create_employee(self):
        """Test creating a new employee"""
        url = reverse('employee-list-create')
        response = self.client.post(url, self.employee_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get().employee_id, 'EMP001')
    
    def test_get_employee_list(self):
        """Test retrieving employee list"""
        Employee.objects.create(**self.employee_data)
        url = reverse('employee-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AttendanceAPITest(APITestCase):
    """Test cases for Attendance API endpoints"""
    
    def setUp(self):
        self.employee = Employee.objects.create(
            employee_id="EMP001",
            full_name="John Doe",
            email="john.doe@example.com",
            department="IT"
        )
        self.attendance_data = {
            "employee": self.employee.id,
            "date": date.today(),
            "status": "Present"
        }
    
    def test_create_attendance(self):
        """Test creating a new attendance record"""
        url = reverse('attendance-list-create')
        response = self.client.post(url, self.attendance_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Attendance.objects.count(), 1)
    
    def test_get_attendance_list(self):
        """Test retrieving attendance list"""
        Attendance.objects.create(**self.attendance_data)
        url = reverse('attendance-list-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
