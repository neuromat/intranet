$(document).ready(function () {

    // ### Book or chapter ###

    var $id_type = $('#id_type');

    //This file should looking for control-group class if django-suit is used.
    if ($(".control-group")[0]){
        var $class = ('.control-group');
    } else {
        var $class = ('.form-row');
    }

    $id_type.each(function() {
        if($(this).val() == 'c'){
            $('#id_chapter').parents($class).show();
            $('#id_start_page').parents($class).show();
            $('#id_end_page').parents($class).show();
        } else{
            $('#id_chapter').parents($class).hide();
            $('#id_start_page').parents($class).hide();
            $('#id_end_page').parents($class).hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'c'){
            $('#id_chapter').parents($class).show();
            $('#id_start_page').parents($class).show();
            $('#id_end_page').parents($class).show();
        } else{
            $('#id_chapter').parents($class).hide();
            $('#id_start_page').parents($class).hide();
            $('#id_end_page').parents($class).hide();
        }
    });
});