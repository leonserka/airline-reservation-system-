from django.db import models

# Create your models here.

FLIGHT_TYPE_CHOICES = [
    ('DOM', 'Domestic'),
    ('INT', 'International')
]

CLASS_CHOICES = [
    ('BASIC', 'Basic'),
    ('REGULAR', 'Regular'),
    ('PLUS', 'Plus')
]

class Flight(models.Model):
    flight_number = models.CharField(max_length=10)
    departure_city = models.CharField(max_length=50)
    arrival_city = models.CharField(max_length=50)
    date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    total_seats = models.IntegerField()
    available_seats = models.IntegerField()
    baggage_allowance = models.IntegerField(default=0)
    flight_type = models.CharField(max_length=3, choices=FLIGHT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.flight_number} | {self.departure_city} → {self.arrival_city} | {self.date}"

from django.contrib.auth.models import User
from django.db import models

class Ticket(models.Model):
    
    PAYMENT_STATUS_CHOICES = [
        ('paid', 'Paid'),
        ('refunded', 'Refunded'),
    ]

    STATUS_CHOICES = [
        ('booked', 'Booked'),
        ('canceled', 'Canceled'),
    ]

    flight = models.ForeignKey('Flight', on_delete=models.CASCADE)
    passenger_name = models.CharField(max_length=50)
    passenger_surname = models.CharField(max_length=50)
    id_number = models.CharField(max_length=11)
    country_code = models.CharField(max_length=10)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    seat_class = models.CharField(max_length=10, choices=CLASS_CHOICES)
    seat_number = models.CharField(max_length=5, blank=True, null=True)
    price_paid = models.DecimalField(max_digits=8, decimal_places=2)
    payment_method = models.CharField(max_length=20)
    
    payment_status = models.CharField(
        max_length=10,
        choices=PAYMENT_STATUS_CHOICES,
        default='paid',  
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='booked',  
    )

    def __str__(self):
        return f"{self.passenger_name} {self.passenger_surname} | {self.flight.flight_number}"

