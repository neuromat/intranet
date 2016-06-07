$(document).ready(function () {

	var $id_local = $("#id_local");

	//This file should looking for control-group class if django-suit is used.
    if ($(".control-group")[0]){
        var $class = ('.control-group');
    } else {
        var $class = ('.form-row');
    }

	$id_local.on('change', (function() {

		if ($("#id_local option:selected").text() == "Numec")
			$id_local.parents($class).next().hide();

		else
			$id_local.parents($class).next().show();
	}));
});