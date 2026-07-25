from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserRegister(models.Model):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
    )

    fullname = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)


    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='user'
    )

    def __str__(self):
        return self.username


class Service(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='services/')

    def __str__(self):
        return self.name


class Appointment(models.Model):
    user = models.ForeignKey(UserRegister, on_delete=models.CASCADE)
    pet_name = models.CharField(max_length=100)
    pet_breed = models.CharField(max_length=100)

    # ✅ CHANGED HERE
    service = models.ForeignKey(Service, on_delete=models.CASCADE)

    appointment_date = models.DateField()
    appointment_time = models.TimeField()

    description = models.TextField(blank=True)

    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    WORK_STATUS_CHOICES = [
        ('Not Done', 'Not Done'),
        ('Done', 'Done'),
    ]

    work_status = models.CharField(max_length=20, choices=WORK_STATUS_CHOICES, default='Not Done')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pet_name} - {self.service} ({self.status})"


class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15, blank=True)
    message = models.TextField()
    reply = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


