// this file also prevents django.jQuery.noConflictvar django = django || {};
// used to run the autocomplete function

var django = django || {};
django.jQuery = jQuery

var yl = yl || {};
yl.jQuery = django.jQuery
