from modeltranslation.translator import translator, TranslationOptions
from .models import Role


class RoleTranslationOptions(TranslationOptions):
    fields = ('name',)


translator.register(Role, RoleTranslationOptions)
