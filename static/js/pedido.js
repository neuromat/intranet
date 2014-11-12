$(document).ready(function () {
    $("#id_type_1").click(function () {
        $("#id_inbound_date").prop('disabled', true);
        $("#id_inbound_date_preference").prop('disabled', true);
    });
    $("#id_type_0").click(function () {
        $("#id_inbound_date").prop('disabled', false);
        $("#id_inbound_date_preference").prop('disabled', false);
    });
});