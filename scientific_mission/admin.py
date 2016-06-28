from forms import *
from models import *
from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from django.utils.translation import ugettext_lazy as _


admin.site.register(Type)


class InlineValidationDate(BaseInlineFormSet):
    def clean(self):
        super(InlineValidationDate, self).clean()

        if any(self.errors):
            return

        previous_date = False
        for form in self.forms:
            start_date = form.cleaned_data.pop('departure', None)
            end_date = form.cleaned_data.pop('arrival', None)

            if previous_date and start_date and previous_date > start_date:
                raise ValidationError(_("The departure date must be greater than the arrival date of the previous "
                                        "route."))

            previous_date = end_date

            if start_date and end_date and start_date > end_date:
                raise ValidationError(_("The arrival date can not be earlier than the departure date."))


class RouteInline(admin.TabularInline):
    model = Route
    extra = 1
    form = RouteForm
    formset = InlineValidationDate
    verbose_name = _('Route')
    verbose_name_plural = _('Routes')


class ScientificMissionAdmin(admin.ModelAdmin):
    fields = ['person', 'amount_paid', 'mission', 'project_activity', 'destination_city']
    list_display = ('id', 'person', 'value', 'mission', 'destination_city')
    list_display_links = ('id',)
    search_fields = ['person__full_name', 'mission__mission', 'project_activity__title']
    inlines = (RouteInline,)
    form = ScientificMissionForm
admin.site.register(ScientificMission, ScientificMissionAdmin)
