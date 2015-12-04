$(document).ready(function () {

    var $status = $('#id_status');
    var $id_type = $('#id_type');
    var $published = $('#id_status_3');
    var $accepted = $('#id_status_2');
    var $submitted = $('#id_status_1');
    var $draft = $('#id_status_0');


    // ### Hide/show "Where will be published?" field ###
    if ($accepted.checked || $published.checked){
        $id_type.parents('.row').show();
    } else {
        $id_type.parents('.row').hide();
    }

    $status.click(function(){
       if ($accepted.is(':checked') || $published.is(':checked')) {
          $id_type.parents('.row').show();
       } else {
          $id_type.parents('.row').hide();
       }
    });


    // ### Hide/show draft inline ###
    if ($draft.checked){
        $('[id^="draft"]').parents('._inline-group').show();
    } else {
        $('[id^="draft"]').parents('._inline-group').hide();
    }

    $status.click(function(){
       if ($draft.is(':checked')) {
          $('[id^="draft"]').parents('._inline-group').show();
       } else {
          $('[id^="draft"]').parents('._inline-group').hide();
       }
    });


    // ### Hide/show submitted inline ###
    if ($submitted.checked){
        $('[id^="submitted"]').parents('._inline-group').show();
    } else {
        $('[id^="submitted"]').parents('._inline-group').hide();
    }

    $status.click(function(){
       if ($submitted.is(':checked')) {
          $('[id^="submitted"]').parents('._inline-group').show();
       } else {
          $('[id^="submitted"]').parents('._inline-group').hide();
       }
    });


    // ### Hide/show event or periodical inline (published) ###
    $id_type.each(function() {
        if($(this).val() == 'p' && $published.is(':checked')){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        } else if($(this).val() == 'e' && $published.is(':checked')){
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').show();
        } else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p' && $published.is(':checked')){
            $('[id^="publishedinperiodical"]').parents('._inline-group').show();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        } else if($(this).val() == 'e' && $published.is(':checked')){
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').show();
        }else{
            $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
            $('[id^="publishedinevent"]').parents('._inline-group').hide();
        }
    });

    $status.click(function(){
       if ($published.is(':checked') && $id_type.val() == 'p') {
          $('[id^="publishedinperiodical"]').parents('._inline-group').show();
       } else {
          $('[id^="publishedinperiodical"]').parents('._inline-group').hide();
       }
    });

    $status.click(function(){
       if ($published.is(':checked') && $id_type.val() == 'e') {
          $('[id^="publishedinevent"]').parents('._inline-group').show();
       } else {
          $('[id^="publishedinevent"]').parents('._inline-group').hide();
       }
    });


    // ### Hide/show event or periodical inline (accepted) ###
    $id_type.each(function() {
        if($(this).val() == 'p' && $accepted.is(':checked')){
            $('[id^="acceptedinperiodical"]').parents('._inline-group').show();
            $('[id^="acceptedinevent"]').parents('._inline-group').hide();
        } else if($(this).val() == 'e' && $accepted.is(':checked')){
            $('[id^="acceptedinperiodical"]').parents('._inline-group').hide();
            $('[id^="acceptedinevent"]').parents('._inline-group').show();
        }else{
            $('[id^="acceptedinperiodical"]').parents('._inline-group').hide();
            $('[id^="acceptedinevent"]').parents('._inline-group').hide();
        }
    });

    $id_type.change(function(){
        if($(this).val() == 'p' && $accepted.is(':checked')){
            $('[id^="acceptedinperiodical"]').parents('._inline-group').show();
            $('[id^="acceptedinevent"]').parents('._inline-group').hide();
        } else if($(this).val() == 'e' && $accepted.is(':checked')){
            $('[id^="acceptedinperiodical"]').parents('._inline-group').hide();
            $('[id^="acceptedinevent"]').parents('._inline-group').show();
        }else{
            $('[id^="acceptedinperiodical"]').parents('._inline-group').hide();
            $('[id^="acceptedinevent"]').parents('._inline-group').hide();
        }
    });

    $status.click(function(){
       if ($accepted.is(':checked') && $id_type.val() == 'p') {
          $('[id^="acceptedinperiodical"]').parents('._inline-group').show();
       } else {
          $('[id^="acceptedinperiodical"]').parents('._inline-group').hide();
       }
    });

    $status.click(function(){
       if ($accepted.is(':checked') && $id_type.val() == 'e') {
          $('[id^="acceptedinevent"]').parents('._inline-group').show();
       } else {
          $('[id^="acceptedinevent"]').parents('._inline-group').hide();
       }
    });

});
