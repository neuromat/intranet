# -*- coding: utf-8 -*-

# This file was created based on what is explained in:
# https://code.djangoproject.com/wiki/InitialSQLDataDiangoORMWay

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'sistema.settings'

from research.models import TypeAcademicWork

# Types of academic work
type = TypeAcademicWork(name="Post-doctoral")
type.save()
type = TypeAcademicWork(name="PhD")
type.save()
type = TypeAcademicWork(name="MSc")
type.save()