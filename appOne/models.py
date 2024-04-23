from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.

# Mahathir Saad Islam, w1907417

class Person(models.Model):
    """
    Represents a person, extending the default User model with additional personal information.
    This class links directly to a User instance and stores personal details.
    """

    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField(verbose_name='date of birth')
    email = models.EmailField(verbose_name='email address', unique=True)
    phone_number = models.CharField(verbose_name='phone number', max_length=17)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Equipment(models.Model):
    """
    Represents a piece of equipment that can be reserved by users.
    Includes details such as type, location, availability, and more.
    """
    id = models.AutoField(primary_key=True)
    type_of_device = models.CharField(max_length=255)
    image = models.ImageField(upload_to='appOne/images/')
    quantity = models.PositiveIntegerField()
    audit = models.DateField(help_text="Please enter the date in YYYY-MM-DD format.")
    device_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    onsite = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"Equipment {self.id}"

class Reservation(models.Model):
     """
    Represents a reservation made by a user for a piece of equipment.
    It links a User with the Equipment they intend to reserve, along with dates and status.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reservations',blank=True, null=True)
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    alerts = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=255, choices=[('approved', 'Approved'), ('rejected', 'Rejected')],blank=True, null=True)
    purpose = models.TextField()
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='reservations', blank=True, null=True)
    def __str__(self):
        return f"Reservation {self.id}"


class Cart(models.Model):
    """
    Represents a shopping cart for a user, holding temporary selections of equipment before final reservation.
    It maintains a relationship between the User and multiple pieces of Equipment.
    """
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='carts')
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='cart_items')
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    purpose = models.TextField()


    def __str__(self):
        return f"Cart {self.id} of {user.first_name} {user.last_name}"
