$(function(){

  // #######################
  // ### Pedido App ###
  // #######################

    $("#id_item").blur(function () {
        var x = document.getElementById("id_item");
        if (x.value != "2" && x.value != "4") {
            $("#id_start_date_0").prop('disabled', false);
            $("#id_start_date_1").prop('disabled', false);
            $("#id_end_date_0").prop('disabled', false);
            $("#id_end_date_1").prop('disabled', false);
        }
        else {
            $("#id_start_date_0").prop('disabled', true);
            $("#id_start_date_1").prop('disabled', true);
            $("#id_end_date_0").prop('disabled', true);
            $("#id_end_date_1").prop('disabled', true);
        }
    });
});