# Register your models here.
from django.contrib import admin
from configuration.models import *
from solo.admin import SingletonModelAdmin

admin.site.register(ProcessNumber, SingletonModelAdmin)
admin.site.register(CepidName, SingletonModelAdmin)
admin.site.register(PrincipalInvestigator, SingletonModelAdmin)
