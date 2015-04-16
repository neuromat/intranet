$(document).ready(function () {

    // ### Duration field ###

    var $id_type = $('#id_type');

    $id_type.each(function() {
        if($(this).val() == 'a' || $(this).val() == 'i'){
            $('#id_paper_status').parents('.row').show();
        } else{
            $('#id_paper_status').parents('.row').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'a' || $(this).val() == 'i'){
            $('#id_paper_status').parents('.row').show();
        } else{
            $('#id_paper_status').parents('.row').hide();
        }
    });

});