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
    }});
}

function data_handler(doc, data) {
    var index = 0;
    while(index != data.length) {
        start_time_id = data[index][0];
        final_time_id = data[index][1];
        event_name    = data[index][3];


        console.log(start_time_id);
        doc.getElementById(start_time_id).style.background = "#000";

        index += 1;

    }
}
