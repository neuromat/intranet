$(document).ready(function () {

    // ### Article ###

    //var $id_type = $('#id_articlestatus_set-0-type');
    var $id_type = $('[id$=type]');


    $id_type.each(function() {
        if($(this).val() == 'p'){
            $('[id$=volume]').parents('.row').show();
            $('[id$=number]').parents('.row').show();
            $('[id$=doi]').parents('.row').show();
            $('[id$=start_page]').parents('.row').show();
            $('[id$=end_page]').parents('.row').show();
        } else{
            $('[id$=volume]').parents('.row').hide();
            $('[id$=number]').parents('.row').hide();
            $('[id$=doi]').parents('.row').hide();
            $('[id$=start_page]').parents('.row').hide();
            $('[id$=end_page]').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p'){
            $('[id$=volume]').parents('.row').show();
            $('[id$=number]').parents('.row').show();
            $('[id$=doi]').parents('.row').show();
            $('[id$=start_page]').parents('.row').show();
            $('[id$=end_page]').parents('.row').show();
        } else{
            $('[id$=volume]').parents('.row').hide();
            $('[id$=number]').parents('.row').hide();
            $('[id$=doi]').parents('.row').hide();
            $('[id$=start_page]').parents('.row').hide();
            $('[id$=end_page]').parents('.row').hide();
        }
    });
});
