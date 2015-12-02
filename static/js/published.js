$(document).ready(function () {

    var $id_type = $('#id_type');

    $id_type.each(function() {
        if($(this).val() == 'p'){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        } else if($(this).val() == 'e'){
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p'){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        } else if($(this).val() == 'e'){
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        }
    });
});
