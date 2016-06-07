$(document).ready(function () {

    // ### Book or chapter ###

    var $id_type = $('#id_funding');

    //This file should looking for control-group class if django-suit is used.
    if ($(".control-group")[0]){
        var $class = ('.control-group');
    } else {
        var $class = ('.form-row');
    }

    $id_type.each(function() {
        if($(this).val() == 'True'){
            $('#id_funding_agency').parents($class).show();
            $('#id_url').parents($class).show();
        } else{
            $('#id_funding_agency').parents($class).hide();
            $('#id_url').parents($class).hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'True'){
            $('#id_funding_agency').parents($class).show();
            $('#id_url').parents($class).show();
        } else{
            $('#id_funding_agency').parents($class).hide();
            $('#id_url').parents($class).hide();
        }
    });
});