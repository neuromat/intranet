$(document).ready(function () {

    var $id_type = $('[id$=type]');

    $id_type.each(function() {
        if($(this).val() == 'j'){
            $('[id$=journal]').parents('.row').show();
        } else{
            $('[id$=journal]').parents('.row').hide();
        }
        if($(this).val() == 'e'){
            $('[id$=event]').parents('.row').show();
        } else{
            $('[id$=event]').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'j'){
            $('[id$=journal]').parents('.row').show();
        } else{
            $('[id$=journal]').parents('.row').hide();
        }
        if($(this).val() == 'e'){
            $('[id$=event]').parents('.row').show();
        } else{
            $('[id$=event]').parents('.row').hide();
        }
    });
});
