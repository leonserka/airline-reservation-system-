from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('', views.flight_list, name='flight_list'),
    path('create-flight/', views.create_flight, name='create_flight'),
    path('book/<int:flight_id>/', views.book_flight, name='book_flight'),
    path('flights/', views.flight_list, name='flight_list'),

    path('book/<int:flight_id>/step1/', views.book_step1, name='book_step1'),
    path('book/<int:flight_id>/step2/', views.book_step2, name='book_step2'),
    path('book/<int:flight_id>/step3/', views.book_step3, name='book_step3'),
    path('book/<int:flight_id>/step4/', views.book_step4, name='book_step4'),
    path('book/success/', views.book_success, name='book_success'),
    
    path('login/', auth_views.LoginView.as_view(template_name='flights/login.html'), name='login'),
    path('logout/', views.custom_logout, name='logout'),  # koristimo custom logout
    path('register/', views.register, name='register'),
    path('save-seat/', views.save_seat, name='save_seat'),
    path('check-booked-flights/', views.check_booked_flights, name='check_booked_flights'),
    path('cancel-booked-flight/<int:ticket_id>/', views.cancel_booked_flight, name='cancel_booked_flight'),
    path('about-ticket/<int:ticket_id>/', views.about_ticket, name='about_ticket'),    
]