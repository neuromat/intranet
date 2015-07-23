$(document).ready(function () {

    // ### Add Unpublished - Type field ###

    var $id_type = $('#id_type');

    $id_type.each(function() {
        if($(this).val() == 'a' || $(this).val() == 'm'){
            $('#id_paper_status').parents('.row').show();
        } else{
            $('#id_paper_status').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'a' || $(this).val() == 'm'){
            $('#id_paper_status').parents('.row').show();
        } else{
            $('#id_paper_status').parents('.row').hide();
        }
    });


    // ### Add Article - Status field ###

    var $id_status = $('#id_status');

    $id_status.each(function() {
        if($(this).val() == 'p'){
            $('#id_volume').parents('.row').show();
            $('#id_number').parents('.row').show();
            $('#id_doi').parents('.row').show();
            $('#id_start_page').parents('.row').show();
            $('#id_end_page').parents('.row').show();
            $('#id_url').parents('.row').show();
        } else{
            $('#id_volume').parents('.row').hide();
            $('#id_number').parents('.row').hide();
            $('#id_doi').parents('.row').hide();
            $('#id_start_page').parents('.row').hide();
            $('#id_end_page').parents('.row').hide();
            $('#id_url').parents('.row').hide();
        }
    });

    $id_status.change(function(){
        if($(this).val() == 'p'){
            $('#id_volume').parents('.row').show();
            $('#id_number').parents('.row').show();
            $('#id_doi').parents('.row').show();
            $('#id_start_page').parents('.row').show();
            $('#id_end_page').parents('.row').show();
            $('#id_url').parents('.row').show();
        } else{
            $('#id_volume').parents('.row').hide();
            $('#id_number').parents('.row').hide();
            $('#id_doi').parents('.row').hide();
            $('#id_start_page').parents('.row').hide();
            $('#id_end_page').parents('.row').hide();
            $('#id_url').parents('.row').hide();
        }
    });
});