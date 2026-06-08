from django.db import models

# Create your models here.
class Customer_Registration(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.Name

class Staff_Request(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.Name

class Admin_Request(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.Name