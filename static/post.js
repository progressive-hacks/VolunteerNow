function register_event(event_id) {
  $.ajax({
    url:"/volunteer",
    method:"POST",

    data: {
        event: event_id,
    },

    success: (response) => {
        $("#result").html(response);
      },

    error: () => {
        $("#result").html("error");
    }
});

}
