from django.db import models

# Create your models here.

class Department(models.Model):
    name = models.CharField(max_length=100)
    floor = models.IntegerField()

    def __str__(self):
        return self.name


designation_choices = [
        ('Associate', 'Associate'),
        ('TL', 'TL'),
        ('Manager', 'Manager'),
    ]

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    address = models.TextField()
    designation = models.CharField(max_length=20, choices=designation_choices)
    reporting_manager = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class EmployeeSalary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    salary = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
