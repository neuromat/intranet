# -*- coding: utf-8 -*-

# This file was created based on what is explained in:
# https://code.djangoproject.com/wiki/InitialSQLDataDiangoORMWay

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'sistema.settings'

from person.models import Person, CitationName

prep = ['da', 'do', 'de', 'dos']

def last_name_and_initials(person_id, names):
    last_name = names[-1]
    initial = ''
    for name in names:
        if name != last_name and name not in prep:
            initial += name[0]
    citation = last_name+','+' '+initial
    citation_name = CitationName(person_id=person_id, name=citation)
    return citation_name


def last_name_and_completed_names(person_id, names):
    last_name = names[-1]
    names_without_last_name = [name for name in names if name != last_name and name not in prep]
    join_names_without_last_name = ' '.join(names_without_last_name)

    citation = last_name+','+' '+join_names_without_last_name
    citation_name = CitationName(person_id=person_id, name=citation)
    return citation_name


def last_name_first_name_and_initials(person_id, names):
    first_letter = ''
    last_name = names[-1]
    first_name = names[0]
    for name in names:
        if name != first_name and name != last_name and name not in prep:
            first_letter += name[0]
    if first_letter != '':
        citation = last_name+','+' '+first_name+' '+first_letter
        citation_name = CitationName(person_id=person_id, name=citation)
        return citation_name
    else:
        return None


# Create the citation name for each person
for person in Person.objects.all():
    # Get full name and id from person. Split the full name.
    full_name = person.full_name
    person_id = person.pk
    names = full_name.split()

    # Imagine a person called João Carlos da Silva.
    # Here the citation would be Silva, JC
    option_01 = last_name_and_initials(person_id, names)
    if CitationName.objects.filter(person_id=person_id, name=option_01).exists() is False:
        option_01.save()

    # Here the citation would be Silva, João Carlos
    option_02 = last_name_and_completed_names(person_id, names)
    if CitationName.objects.filter(person_id=person_id, name=option_02).exists() is False:
        option_02.save()

    # Here the citation would be Silva, João C
    option_03 = last_name_first_name_and_initials(person_id, names)
    if option_03 is not None and CitationName.objects.filter(person_id=person_id, name=option_03).exists() is False:
        option_03.save()