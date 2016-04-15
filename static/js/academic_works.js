$(document).ready(function () {

    // ### Book or chapter ###

    var $id_type = $('#id_funding');

    $id_type.each(function() {
        if($(this).val() == 'True'){
            $('#id_funding_agency').parents('.row').show();
            $('#id_url').parents('.row').show();
        } else{
            $('#id_funding_agency').parents('.row').hide();
            $('#id_url').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'True'){
            $('#id_funding_agency').parents('.row').show();
            $('#id_url').parents('.row').show();
        } else{
            $('#id_funding_agency').parents('.row').hide();
            $('#id_url').parents('.row').hide();
        }
    });
});