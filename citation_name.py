# -*- coding: utf-8 -*-

# This file was created based on what is explained in:
# https://code.djangoproject.com/wiki/InitialSQLDataDiangoORMWay

from os import environ
environ['DJANGO_SETTINGS_MODULE'] = 'sistema.settings'

from person.models import Person, CitationName

prep = ['da', 'do', 'de', 'dos']

# Create the citation name for each person
for person in Person.objects.all():
    # Get full name and id from person. Split the full name.
    full_name = person.full_name
    person_id = person.pk
    names = full_name.split()

    # Imagine a person called João Carlos da Silva
    # Here the citation would be Silva, JC
    initial = ''
    last_name = names[-1]

    for name in names:
        if name != last_name and name not in prep:
            initial += name[0]
    citation = last_name+','+' '+initial
    citation_name = CitationName(person_id=person_id, name=citation)

    if CitationName.objects.filter(person_id=person_id, name=citation_name).exists() is False:
        citation_name.save()

    # Here the citation would be Silva, João Carlos
    names_without_last_name = [name for name in names if name != last_name and name not in prep]
    join_names_without_last_name = ' '.join(names_without_last_name)

    citation2 = last_name+','+' '+join_names_without_last_name
    citation_name2 = CitationName(person_id=person_id, name=citation2)

    if CitationName.objects.filter(person_id=person_id, name=citation_name2).exists() is False:
        citation_name2.save()

    # Here the citation would be Silva, João C
    first_letter = ''
    first_name = names_without_last_name[0]
    for name in names_without_last_name:
        if name != first_name:
            first_letter += name[0]
    if first_letter != '':
        citation3 = last_name+','+' '+first_name+' '+first_letter
        citation_name3 = CitationName(person_id=person_id, name=citation3)

    if CitationName.objects.filter(person_id=person_id, name=citation_name3).exists() is False:
        citation_name3.save()

