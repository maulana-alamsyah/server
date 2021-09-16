<script>
    //ambil id approve button
    $("#approve-button").submit(function (e) {
        e.preventDefault();
        // make POST ajax call
        $.ajax({
            type: 'POST',
            url: "/approve/",
            data: {
                    'filename' : {{filename}}
                    },
            success: function (response) {
                $(this).hide()
            },
            error: function (response) {
                // alert the error if any error occured
                alert(response["message"]);
            }
        })
    })
</script>
