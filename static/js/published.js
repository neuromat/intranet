$(document).ready(function () {

    var $id_type = $('[id$=type]');

    $id_type.each(function() {
        if($(this).val() == 'p'){
            $('[id$=periodical]').parents('.row').show();
            $('[id$=date]').parents('.row').show();
            $('[id$=event]').parents('.row').hide();
        } else if($(this).val() == 'e'){
            $('[id$=event]').parents('.row').show();
            $('[id$=periodical]').parents('.row').hide();
            $('[id$=date]').parents('.row').hide();
        } else{
            $('[id$=periodical]').parents('.row').hide();
            $('[id$=event]').parents('.row').hide();
            $('[id$=date]').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p'){
            $('[id$=periodical]').parents('.row').show();
            $('[id$=date]').parents('.row').show();
            $('[id$=event]').parents('.row').hide();
        } else if($(this).val() == 'e'){
            $('[id$=event]').parents('.row').show();
            $('[id$=periodical]').parents('.row').hide();
            $('[id$=date]').parents('.row').hide();
        } else{
            $('[id$=periodical]').parents('.row').hide();
            $('[id$=event]').parents('.row').hide();
            $('[id$=date]').parents('.row').hide();
        }
    });
});
