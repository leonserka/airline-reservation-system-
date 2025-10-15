document.addEventListener("DOMContentLoaded", function() {
    const countrySelect = document.getElementById('id_country_code');
    if (countrySelect) {
        $(countrySelect).select2({
            placeholder: "Select a country code",
            allowClear: true
        });
    }
});
