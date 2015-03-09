$(document).ready(function () {
    if (!id_type_0.checked && !id_type_1.checked){
        $("#id_institution").parents('.row').hide();
        $("#id_department").parents('.row').hide();
    }
    $("#id_type_1").click(function () {
        $("#id_inbound_date").parents('.row').hide();
        $("#id_inbound_date_preference").parents('.row').hide();
    });
    $("#id_type_0").click(function () {
        $("#id_inbound_date").parents('.row').show();
        $("#id_inbound_date_preference").parents('.row').show();
    });
});