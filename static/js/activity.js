$(document).ready(function () {

    // ### Duration field ###

    var $id_duration = $('#id_duration');

    //This file should looking for control-group class if django-suit is used.
    if ($(".control-group")[0]){
        var $class = ('.control-group');
    } else {
        var $class = ('.form-row');
    }

    $id_duration.each(function() {
        if($(this).val() == 'Other'){
            $('#id_other_duration').parents($class).show();
        } else{
            $('#id_other_duration').parents($class).hide();
        }
    });

    $id_duration.change(function(){
        if($(this).val() == 'Other'){
            $('#id_other_duration').parents($class).show();
        } else{
            $('#id_other_duration').parents($class).hide();
        }
    });

});