from django.db import models

# Create your models here.
class Staff_Registration(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.Name

class Admin_Registration(models.Model):
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=100)
    Password = models.CharField(max_length=100)
    def __str__(self):
        return self.Name

class PredictionHistory(models.Model):
    STATUS_CHOICES = [('Admin', 'Admin'), ('Staff', 'Staff'), ('Customer', 'Customer')]
    Predict_ID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=20, choices=STATUS_CHOICES)
    Email = models.EmailField()
    Make = models.CharField(max_length=30)
    Model = models.CharField(max_length=30)
    Year = models.IntegerField()
    Engine_HP = models.IntegerField()
    Engine_Cylinders = models.IntegerField()
    Transmission_Type = models.CharField(max_length=30)
    Driven_Wheels = models.CharField(max_length=30)
    Market_Category = models.CharField(max_length=30)
    Vehicle_Size = models.CharField(max_length=30)
    Vehicle_Style = models.CharField(max_length=30)
    highway_MPG = models.IntegerField()
    city_mpg = models.IntegerField()
    Popularity = models.IntegerField()
    MSRP = models.IntegerField()

class RecommandationHistory(models.Model):
    STATUS_CHOICES = [('Admin', 'Admin'), ('Staff', 'Staff'), ('Customer', 'Customer')]
    Recommandation_ID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=20, choices=STATUS_CHOICES)
    Email = models.EmailField()
    Brand = models.CharField(max_length=30)
    Model = models.CharField(max_length=30)
    Data = models.JSONField()

class NotificationModel(models.Model):
    ROLE_CHOICES = [('All', 'All'), ('Admin', 'Admin'), ('Staff', 'Staff'), ('Customer', 'Customer')]
    Notification_ID = models.AutoField(primary_key=True)
    Role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    Title = models.CharField(max_length=100)
    Message = models.TextField()
    Date = models.DateTimeField(auto_now_add=True)

class Service_Request(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved')]
    Service_ID = models.AutoField(primary_key=True)
    Name = models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Phone_No = models.CharField(max_length=30)
    Service_Type = models.CharField(max_length=30)
    Brand = models.CharField(max_length=30)
    Model = models.CharField(max_length=30)
    Number = models.CharField(max_length=30)
    Distance = models.IntegerField()
    Problem = models.TextField()
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

class Service_History(models.Model):
    Service_ID = models.IntegerField(primary_key=True)
    Name = models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Phone_No = models.CharField(max_length=30)
    Service_Type = models.CharField(max_length=30)
    Brand = models.CharField(max_length=30)
    Model = models.CharField(max_length=30)
    Number = models.CharField(max_length=30)
    Distance = models.IntegerField()
    Problem = models.TextField()

class CarRent(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Delivered', 'Delivered')]
    Rent_ID = models.AutoField(primary_key=True)
    Car_ID = models.IntegerField()
    Name = models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Phone_No = models.CharField(max_length=30)
    Pickup_Date = models.DateField(null=True, blank=True)
    Return_Date = models.DateField(null=True, blank=True)
    Address = models.TextField()
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

class activities(models.Model):
    Role = models.CharField(max_length=30)
    Email = models.CharField(max_length=30)
    Activity = models.CharField(max_length=30)
    Date = models.DateTimeField(auto_now_add=True)

class CarOrder(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Delivered', 'Delivered')]
    Order_ID = models.AutoField(primary_key=True)
    Car_ID = models.IntegerField()
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=15)
    Address = models.TextField()
    Payment_Mode = models.CharField(max_length=50, default='Cash')
    Delivery_Type = models.CharField(max_length=50, default='Home Delivery')
    Order_Date = models.DateField(auto_now_add=True)
    Delivery_Date = models.DateField(blank=True, null=True)
    Message = models.TextField(blank=True, null=True)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    def __str__(self):
        return f"Order {self.Order_ID} - Car {self.Car_ID}"

class CarSelling(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected'), ('Delivered', 'Delivered')]
    Sell_ID = models.AutoField(primary_key=True)
    Car_ID = models.IntegerField()
    Name = models.CharField(max_length=100)
    Email = models.CharField(max_length=100)
    Phone_No = models.CharField(max_length=15)
    Status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    Date = models.DateTimeField(auto_now_add=True)
    