$(document).ready(function () {

    // ### Book or chapter ###

    var $id_type = $('#id_type');

    $id_type.each(function() {
        if($(this).val() == 'c'){
            $('#id_chapter').parents('.row').show();
            $('#id_start_page').parents('.row').show();
            $('#id_end_page').parents('.row').show();
        } else{
            $('#id_chapter').parents('.row').hide();
            $('#id_start_page').parents('.row').hide();
            $('#id_end_page').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'c'){
            $('#id_chapter').parents('.row').show();
            $('#id_start_page').parents('.row').show();
            $('#id_end_page').parents('.row').show();
        } else{
            $('#id_chapter').parents('.row').hide();
            $('#id_start_page').parents('.row').hide();
            $('#id_end_page').parents('.row').hide();
        }
    });
});