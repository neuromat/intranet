# -*- coding: utf-8 -*-

# This file was created based on what is explained in:
# https://code.djangoproject.com/wiki/InitialSQLDataDiangoORMWay

from os import environ
from person.models import Role
from research.models import TypeAcademicWork

environ['DJANGO_SETTINGS_MODULE'] = 'sistema.settings'

# Types of academic work
type = TypeAcademicWork(name="Post-doctoral")
type.save()
type = TypeAcademicWork(name="PhD")
type.save()
type = TypeAcademicWork(name="MSc")
type.save()

# Person roles
role = Role(name="Principal Investigator")
role.save()
role = Role(name="Co-principal Investigator")
role.save()
role = Role(name="Associate Investigator")
role.save()
