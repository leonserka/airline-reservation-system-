from django import forms
from .models import Flight, Ticket, CLASS_CHOICES
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .country_codes import COUNTRY_CODES

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_number', 'departure_city', 'arrival_city',
            'date', 'departure_time', 'arrival_time',
            'price', 'total_seats', 'available_seats',
            'baggage_allowance', 'flight_type'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'departure_time': forms.TimeInput(attrs={'type': 'time'}),
            'arrival_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FlightSearchForm(forms.Form):
    departure_city = forms.ChoiceField(choices=[], label="Departure")
    arrival_city = forms.ChoiceField(choices=[], label="Arrival")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        departures = Flight.objects.values_list('departure_city', flat=True).distinct()
        self.fields['departure_city'].choices = [(c, c) for c in departures]

        arrivals = Flight.objects.values_list('arrival_city', flat=True).distinct()
        self.fields['arrival_city'].choices = [(c, c) for c in arrivals]

        self.routes = {}
        for dep in departures:
            valid_arrivals = Flight.objects.filter(departure_city=dep).values_list('arrival_city', flat=True).distinct()
            self.routes[dep] = list(valid_arrivals)

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['passenger_name', 'passenger_surname', 'id_number', 'country_code', 'phone_number', 'seat_class', 'seat_number', 'payment_method']

class PassengerForm(forms.ModelForm):
    country_code = forms.ChoiceField(choices=COUNTRY_CODES)

    class Meta:
        model = Ticket
        fields = ['passenger_name', 'passenger_surname', 'id_number', 'country_code', 'phone_number', 'email']
        widgets = {
            'id_number': forms.TextInput(attrs={'maxlength': 11}),
            'email': forms.EmailInput(),
        }

class ClassForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_class']

class SeatForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_number']

class PaymentForm(forms.Form):
    card_number = forms.CharField(
        max_length=16,
        min_length=16,
        label="Card Number",
        widget=forms.TextInput(attrs={'placeholder': '1234123412341234'})
    )
    expiry_date = forms.DateField(
        label="Expiry Date (MM/YY)",
        input_formats=['%m/%y', '%m/%Y'],
        widget=forms.TextInput(attrs={'placeholder': 'MM/YY'})
    )
    cvv = forms.CharField(
        max_length=3,
        min_length=3,
        label="CVV",
        widget=forms.PasswordInput(attrs={'placeholder': '123'})
    )

class SeatSelectionForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['seat_class', 'seat_number']

    def __init__(self, *args, flight=None, **kwargs):
        self.flight = flight
        super().__init__(*args, **kwargs) 
        
        if self.flight:
            taken_seats = self.flight.ticket_set.values_list('seat_number', flat=True)
            all_seats = [str(i) for i in range(1, self.flight.total_seats+1)]
            available_seats = [s for s in all_seats if s not in taken_seats]
            self.fields['seat_number'].widget = forms.Select(choices=[(s,s) for s in available_seats])


