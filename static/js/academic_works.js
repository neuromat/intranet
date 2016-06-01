$(document).ready(function () {

    // ### Book or chapter ###

    var $id_type = $('#id_funding');

    $id_type.each(function() {
        if($(this).val() == 'True'){
            $('#id_funding_agency').parents('.control-group').show();
            $('#id_url').parents('.control-group').show();
        } else{
            $('#id_funding_agency').parents('.control-group').hide();
            $('#id_url').parents('.control-group').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'True'){
            $('#id_funding_agency').parents('.control-group').show();
            $('#id_url').parents('.control-group').show();
        } else{
            $('#id_funding_agency').parents('.control-group').hide();
            $('#id_url').parents('.control-group').hide();
        }
    });
});