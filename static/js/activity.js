$(document).ready(function () {

    // ### Duration field ###

    var $id_duration = $('#id_duration');

    $id_duration.each(function() {
        if($(this).val() == 'Other'){
            $('#id_other_duration').parents('.row').show();
        } else{
            $('#id_other_duration').parents('.row').hide();
        }
    });

    $id_duration.change(function(){
        if($(this).val() == 'Other'){
            $('#id_other_duration').parents('.row').show();
        } else{
            $('#id_other_duration').parents('.row').hide();
        }
    });

});