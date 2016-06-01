$(document).ready(function () {

    // ### Book or chapter ###

    var $id_type = $('#id_type');

    $id_type.each(function() {
        if($(this).val() == 'c'){
            $('#id_chapter').parents('.control-group').show();
            $('#id_start_page').parents('.control-group').show();
            $('#id_end_page').parents('.control-group').show();
        } else{
            $('#id_chapter').parents('.control-group').hide();
            $('#id_start_page').parents('.control-group').hide();
            $('#id_end_page').parents('.control-group').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'c'){
            $('#id_chapter').parents('.control-group').show();
            $('#id_start_page').parents('.control-group').show();
            $('#id_end_page').parents('.control-group').show();
        } else{
            $('#id_chapter').parents('.control-group').hide();
            $('#id_start_page').parents('.control-group').hide();
            $('#id_end_page').parents('.control-group').hide();
        }
    });
});