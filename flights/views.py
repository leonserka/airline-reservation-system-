from django.shortcuts import render, redirect, get_object_or_404
from .forms import FlightForm
from .models import Flight, Ticket
from django.contrib.auth import login,logout
from .forms import RegisterForm, FlightSearchForm, TicketForm, PassengerForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def home(request):
    return render(request, "flights/home.html")

def create_flight(request):
    if request.method == 'POST':
        form = FlightForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('flight_list')
    else:
        form = FlightForm()
    return render(request, 'flights/create_flight.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_staff = False 
            user.save()
            login(request, user)  
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'flights/register.html', {'form': form})


def custom_logout(request):
    logout(request)
    return redirect('home')

def flight_list(request):
    form = FlightSearchForm(request.GET or None)
    flights = Flight.objects.none()
    available_dates = []

    dep = request.GET.get('departure_city')
    arr = request.GET.get('arrival_city')

    if dep and arr:
        flights_for_dates = Flight.objects.filter(departure_city=dep, arrival_city=arr)
        available_dates = [f.date.strftime("%Y-%m-%d") for f in flights_for_dates]
    else:
        flights_for_dates = Flight.objects.all()
        available_dates = [f.date.strftime("%Y-%m-%d") for f in flights_for_dates]

    if dep and arr:
        flights = flights_for_dates 
        selected_date = request.GET.get('date')
        if selected_date:
            flights = flights.filter(date=selected_date)  
    else:
        flights = Flight.objects.none()  

    routes_dict = {}
    for flight in Flight.objects.all():
        routes_dict.setdefault(flight.departure_city, [])
        if flight.arrival_city not in routes_dict[flight.departure_city]:
            routes_dict[flight.departure_city].append(flight.arrival_city)

    return render(request, 'flights/flight_list.html', {
        'form': form,
        'flights': flights,
        'available_dates': available_dates,
        'routes': routes_dict
    })

@login_required
def book_flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.flight = flight
            ticket.price_paid = flight.price
            ticket.save()
            return redirect('flight_list')
    else:
        form = TicketForm()
    
    return render(request, 'flights/book_flight.html', {'form': form, 'flight': flight})


# STEP 1: Passenger Details
@login_required
def book_step1(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    total_price = float(flight.price)

    if request.method == 'POST':
        form = PassengerForm(request.POST)
        if form.is_valid():
            request.session['passenger_data'] = form.cleaned_data  
            return redirect('book_step2', flight_id=flight.id)
    else:
        form = PassengerForm()

    return render(request, 'flights/book_step1.html', {
        'flight': flight,
        'form': form,
        'total_price': total_price
    })


# STEP 2: Choose Class
@login_required
def book_step2(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    base_price = flight.price

    if request.method == 'POST':
        selected_class = request.POST.get('seat_class')
        request.session['seat_class'] = selected_class

        class_prices = {'BASIC': 0, 'REGULAR': 30, 'PLUS': 45}
        total_price = base_price + class_prices.get(selected_class, 0)
        request.session['total_price'] = float(total_price)

        return redirect('book_step3', flight_id=flight.id)

    seat_options = [
        {'name': 'BASIC', 'price': 0},
        {'name': 'REGULAR', 'price': 30},
        {'name': 'PLUS', 'price': 45},
    ]

    return render(request, 'flights/book_step2.html', {
        'flight': flight,
        'seat_options': seat_options,
        'total_price': base_price
    })

@login_required
def book_step3(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)

    taken_seats = flight.ticket_set.values_list('seat_number', flat=True)
    all_seats = [str(i) for i in range(1, flight.total_seats + 1)] 
    available_seats = [s for s in all_seats if s not in taken_seats]

    seat_positions = []
    for row in range(1, 18):  
        row_seats = {'left': [], 'right': []}  
        for seat in range(1, 5):  
            seat_id = (row - 1) * 4 + seat
            top = 105 + (row - 1) * 25.1
            if seat <= 2:
                left = 150 + (seat - 1) * 23  
                row_seats['left'].append({'seat_id': seat_id, 'top': top, 'left': left, 'occupied': str(seat_id) in taken_seats})
            else:
                right = 150 + (seat - 3) * 23  
                row_seats['right'].append({'seat_id': seat_id, 'top': top, 'left': right, 'occupied': str(seat_id) in taken_seats})

        seat_positions.append(row_seats)

    if request.method == 'POST':
        selected_seat = request.POST.get('selected_seat')
        if selected_seat:
            request.session['selected_seat'] = selected_seat  
            return redirect('book_step4', flight_id=flight.id)

    total_price = request.session.get('total_price', float(flight.price))

    return render(request, 'flights/book_step3.html', {
        'flight': flight,
        'total_price': total_price,
        'available_seats': available_seats,
        'seat_positions': seat_positions, 
        'taken_seats': taken_seats 
    })

# STEP 4: Payment
@login_required
def book_step4(request, flight_id):
    flight = get_object_or_404(Flight, id=flight_id)
    passenger_data = request.session.get('passenger_data', {})
    seat_class = request.session.get('seat_class')
    seat_number = request.session.get('selected_seat')
    country_code = passenger_data.get('country_code')
    total_price = request.session.get('total_price', float(flight.price))

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            ticket = Ticket.objects.create(
                flight=flight,
                passenger_name=passenger_data.get('passenger_name'),
                passenger_surname=passenger_data.get('passenger_surname'),
                id_number=passenger_data.get('id_number'),
                email=passenger_data.get('email'),
                phone_number=passenger_data.get('phone_number'),
                seat_class=seat_class,
                seat_number=seat_number,
                country_code=country_code,
                price_paid=total_price,
                payment_method='Card'
            )

            request.session['ticket_id'] = ticket.id
            return redirect('book_success')
    else:
        form = PaymentForm()

    return render(request, 'flights/book_step4.html', {
        'form': form,
        'flight': flight,
        'total_price': total_price
    })

# SUCCESS PAGE
@login_required
def book_success(request):
    ticket_id = request.session.pop('ticket_id', None)
    if not ticket_id:
        return redirect('flight_list')

    ticket = get_object_or_404(Ticket, id=ticket_id)

    ticket.payment_status = 'Paid'
    ticket.save()  

    return render(request, 'flights/book_success.html', {
        'ticket': ticket,
        'payment_status': ticket.payment_status  
    })

@csrf_exempt
def save_seat(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        selected_seat = data.get('selected_seat')
        request.session['selected_seat'] = selected_seat  
        print(f"Selected seat saved: {selected_seat}")  
        return JsonResponse({'status': 'success', 'selected_seat': selected_seat})
    return JsonResponse({'status': 'failed'})


from django.shortcuts import render, get_object_or_404, redirect
from .models import Ticket

def check_booked_flights(request):
    if not request.user.is_authenticated:
        return redirect('login')  

    tickets = Ticket.objects.filter(email=request.user.email)  

    return render(request, 'flights/check_booked_flights.html', {
        'tickets': tickets
    })



from django.shortcuts import get_object_or_404, redirect, render
from .models import Ticket
@login_required
def cancel_booked_flight(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if ticket.seat_class == "PLUS":
        ticket.payment_status = 'refunded'
        ticket.status = 'canceled'  
        ticket.seat_number = None  
        ticket.save()

        return redirect('check_booked_flights') 
    else:
        return render(request, 'flights/error.html', {
            'message': 'You can only cancel PLUS class tickets.'
        })

from django.shortcuts import get_object_or_404, render
from .models import Ticket

def about_ticket(request, ticket_id):

    ticket = get_object_or_404(Ticket, id=ticket_id)

    can_cancel = True if ticket.seat_class == "PLUS" else False

    return render(request, 'flights/about_ticket.html', {
        'ticket': ticket,
        'can_cancel': can_cancel
    })

