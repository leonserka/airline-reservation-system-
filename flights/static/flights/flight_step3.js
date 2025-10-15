document.addEventListener("DOMContentLoaded", function() {
    const seats = document.querySelectorAll('.seat');

    seats.forEach(seat => {
        seat.addEventListener('click', function() {
            if (seat.classList.contains('occupied')) return; 

            if (seat.classList.contains('canceled')) {
                seat.classList.remove('canceled');
                seat.classList.add('available');
            }

            seats.forEach(s => {
                if (!s.classList.contains('occupied')) {
                    s.classList.remove('selected');
                }
            });

            seat.classList.add('selected');
            document.getElementById('selected-seat-text').innerText = "Selected Seat: " + seat.dataset.seat;
            document.querySelector('.continue-btn').disabled = false;

            fetch('/save-seat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                },
                body: JSON.stringify({ selected_seat: seat.dataset.seat })
            });
        });
    });
});
