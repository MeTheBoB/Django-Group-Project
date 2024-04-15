from django.db import models
from django.contrib.auth.models import User
# Create your models here.






class Person(models.Model):
    person_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    surname = models.CharField(max_length=30)
    date_of_birth = models.DateField(('date of birth'))
    email = models.EmailField(('email address'), unique=True)
    phone_number = models.CharField(('phone number'), max_length=17)
    def __str__(self):
        return self.person_id


class Student(Person):
    course = models.CharField(max_length=255)

    def __str__(self):
        return self.person_id


class Admin(Person):

    def __str__(self):
        return self.person_id

STAFF_TYPES = (
    ('parttime', 'Part time'),
    ('fulltime', 'Full time'),
    ('visitor', 'Visitor'),
)

class Staff(Person):
    type = models.CharField(max_length=255, choices=STAFF_TYPES)

    def __str__(self):
        return self.person_id



class Reservation(models.Model):
    reservation_id = models.AutoField(primary_key=True)
    booking_start_date = models.DateTimeField()
    booking_end_date = models.DateTimeField()
    alerts = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=[('approved', 'Approved'), ('rejected', 'Rejected')])
    purpose = models.TextField(blank=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return self.reservation_id

class Equipment(models.Model):
    equipment_id = models.AutoField(primary_key=True)
    type_of_device = models.CharField(max_length=255)
    image = models.ImageField(upload_to='appOne/images/')
    quantity = models.PositiveIntegerField()
    audit = models.DateField()
    device_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255)
    comments = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=255)
    onsite = models.BooleanField(default=True)
    availability = models.BooleanField(default=True)

    reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='equipment', null=True, blank=True)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipment')

    def __str__(self):
        return str(self.equipment_id) 
