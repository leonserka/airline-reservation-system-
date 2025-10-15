document.addEventListener("DOMContentLoaded", function() {
    var availableDates = window.availableDates || [];

    flatpickr("#flight-date", {
        dateFormat: "Y-m-d",
        enable: availableDates,
        locale: { firstDayOfWeek: 1 }
    });

    const dep = document.getElementById("id_departure_city");
    const arr = document.getElementById("id_arrival_city");
    const routes = window.routes || {};

    function filterArrivalOptions() {
        const selectedDep = dep.value;
        const validArrivals = routes[selectedDep] || [];

        for (let option of arr.options) {
            option.disabled = !validArrivals.includes(option.value);
            option.hidden = !validArrivals.includes(option.value);
        }

        if (!validArrivals.includes(arr.value)) {
            arr.value = "";
        }
    }

    function disableSameOption() {
        for (let option of arr.options) {
            option.disabled = option.value === dep.value;
        }
    }

    dep.addEventListener("change", filterArrivalOptions);
    dep.addEventListener("change", disableSameOption);
    arr.addEventListener("change", disableSameOption);

    filterArrivalOptions();
    disableSameOption();
});
