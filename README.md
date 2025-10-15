# ✈️ Airline Reservation System (Django)

Airline Reservation System je web aplikacija izrađena u **Django frameworku** koja omogućuje korisnicima pretragu, rezervaciju i otkazivanje avionskih karata.  
Administrator može dodavati nove letove, dok korisnici mogu pregledavati i upravljati vlastitim rezervacijama.

---

## 🚀 Funkcionalnosti

### 👤 Korisnici
- Registracija i prijava korisnika  
- Pretraga dostupnih letova po polaznom i dolaznom gradu te datumu  
- Višestupanjski proces rezervacije:
  1. Unos osobnih podataka  
  2. Odabir klase sjedala (Basic, Plus, Premium)  
  3. Odabir sjedala na mapi aviona  
  4. Pregled i potvrda rezervacije  
- Pregled svih svojih kupljenih karata (Check Booked Flights)  
- Pregled detalja pojedine karte (About Ticket)  
- Otkazivanje karte (Cancel Ticket) – dostupno samo za **PLUS** klasu  
- Kada se karta otkaže, sjedalo se automatski oslobađa i postaje ponovno dostupno  

### 🧑‍💼 Administrator
- Dodavanje, uređivanje i brisanje letova kroz **Django admin panel**  
- Pregled svih kupljenih karata i statusa plaćanja  

---

## 🗄️ Modeli

### `Flight`
Informacije o letu:
- Broj leta, polazni i dolazni grad  
- Datum, vrijeme i cijena  

### `Ticket`
Informacije o rezervaciji:
- Putnik (ime, prezime, OIB, email, telefon, država)  
- Let (ForeignKey → Flight)  
- Klasa sjedala i broj sjedala  
- Način plaćanja  
- **Payment Status:** `Paid` / `Refunded`  
- **Status:** `Booked` / `Canceled`  

---

## ⚙️ Pokretanje projekta lokalno

### 1️⃣ Kloniraj repozitorij
```bash
git clone https://github.com/korisnicko_ime/airline_reservation_django.git
cd airline_reservation_django
