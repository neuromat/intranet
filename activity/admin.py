from django.contrib import admin
from activity.models import *
#from django.utils.translation import ugettext_lazy as _

admin.site.register(TrainingProgram)
admin.site.register(Seminar)
admin.site.register(ScientificMission)
admin.site.register(Meeting)
admin.site.register(GeneralEvent)
