
$(function() {

    var $new_location_form = $('#new_location_form');
    var $location_btn = $('#new_location_btn');
    var $user_location_form = $('#user_location_form');
    var $user_location_btn = $('#user_location_btn');

    $location_btn.on('click', function(event) {
        event.preventDefault();

        var $formData = {
            name: $new_location_form.find('#new_name').val(),
            longitude: $new_location_form.find('#new_longitude').val(),
            latitude: $new_location_form.find('#new_latitude').val(),
        };


        var elevation_url = 'https://elevation-api.io/api/elevation?points=(' +
            $formData.longitude + ','  + $formData.latitude + ')';


        $.ajax({
            url: elevation_url,
            method: 'GET'

        }).done(function(response) {
            $formData.elevation = response.elevations[0].elevation;
            $.ajax({
                url: 'http://127.0.0.1:8000/locations/',
                method: 'POST',
                data: $formData,
            }).done(function(response) {
                console.log($formData);
                alert("Lokacja dodana");
                location.reload();


            });



        });


    });

    $user_location_btn.on('click', function(event) {
        event.preventDefault();

        var $userFormData = {
            user_name: $user_location_form.find('#user_name').val(),
            user_longitude: $user_location_form.find('#user_longitude').val(),
            user_latitude: $user_location_form.find('#user_latitude').val(),
            perimeter: $user_location_form.find('#perimeter').val()
        };



        $.ajax({
                url: 'http://127.0.0.1:8000/locations/',
                method: 'GET',
                data: $userFormData,
            }).done(function(response) {
                console.log($userFormData);
                alert("Pozycja przesłana");
                location.reload();


            });




    });




});