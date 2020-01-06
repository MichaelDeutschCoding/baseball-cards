    $("#comment-form").submit(function(event) {
        event.preventDefault();
        let that = this;
        let form_data = $(this).serializeArray();
        let final_form_data = new Object();
        $.each(form_data, function(index, element) {
            final_form_data[element['name']] = element['value']
        });
        let csrf_token = final_form_data['csrfmiddlewaretoken'];
        delete final_form_data['csrfmiddlewaretoken'];
        console.log(form_data)
        $.ajax({
            url: "/offers/{{ offer.pk }}/comments",
            type: "POST",
            data: JSON.stringify(final_form_data),
            contentType: "application/json",
            headers: {
                'X-CSRFToken': csrf_token
            }
        }).done(function(response) {
            $(that).trigger("reset");
        });
    });

