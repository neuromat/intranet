from scientific_mission.models import *
from scientific_mission.forms import *
from suit.admin import SortableTabularInline
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

        for form in self.forms:
            start_date = form.cleaned_data.pop('departure', None)
            end_date = form.cleaned_data.pop('arrival', None)

            if start_date and end_date and start_date > end_date:
                raise ValidationError(_("The arrival date can not be earlier than the departure date."))


class RouteInline(SortableTabularInline):
    model = Route
    sortable = 'order'
    extra = 1
    form = RouteForm
    formset = InlineValidationDate


class ScientificMissionAdmin(admin.ModelAdmin):
    fields = ['person', 'amount_paid', 'mission', 'project_activity', 'destination_city']
    list_display = ('id', 'person', 'value', 'mission', 'destination_city')
    list_display_links = ('id',)
    search_fields = ['person__full_name', 'mission__mission', 'project_activity__title']
    inlines = (RouteInline,)
    form = ScientificMissionForm
admin.site.register(ScientificMission, ScientificMissionAdmin)
