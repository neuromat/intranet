# Register your models here.
from django.contrib import admin
from solo.admin import SingletonModelAdmin
from configuration.models import ProcessNumber, CepidName, PrincipalInvestigator

admin.site.register(ProcessNumber, SingletonModelAdmin)
admin.site.register(CepidName, SingletonModelAdmin)
admin.site.register(PrincipalInvestigator, SingletonModelAdmin)
