# -*- coding: utf-8 -*-
from django.shortcuts import render
from person.models import Person, CitationName
from django.contrib.auth.decorators import login_required


prep = ['da', 'do', 'de', 'dos']


def first_letter_of_the_name(names):
    letter = ''
    last_name = names[-1]
    for name in names:
        if name != last_name and name not in prep:
            letter += name[0]
    return letter


def names_without_last_name(names):
    last_name = names[-1]
    citation_name = [name for name in names if name != last_name and name not in prep]
    citation_name = ' '.join(citation_name)
    return citation_name


def first_name_and_first_letter(names):
    first_letter = ''
    first_name = names[0]
    last_name = names[-1]
    for name in names:
        if name != first_name and name != last_name and name not in prep:
            first_letter += name[0]
    if first_letter != '':
        citation_name = first_name+' '+first_letter
        return citation_name
    else:
        citation_name = first_name
        return citation_name


def generate_citation_names(person):

    # Get full name and id from person.
        full_name = person.full_name
        person_id = person.pk

        # Split the full name.
        split_name = full_name.split()

        # Get the last name
        last_name = split_name[-1]

        # Get the first letter of the name except the last name
        letters = first_letter_of_the_name(split_name)

        # Get names without last name
        almost_full_name = names_without_last_name(split_name)

        # Get first name and first letter of the middle name
        first_name_letter_middle_name = first_name_and_first_letter(split_name)

        # Imagine a person called João Carlos da Silva.
        # Here the citation would be "Silva, JC"
        citation_name_01 = CitationName(person_id=person_id, name=last_name+','+' '+letters)
        if CitationName.objects.filter(person_id=person_id, name=citation_name_01).exists() is False:
            citation_name_01.save()

        # Here the citation would be "Silva, João Carlos"
        citation_name_02 = CitationName(person_id=person_id, name=last_name+','+' '+almost_full_name)
        if CitationName.objects.filter(person_id=person_id, name=citation_name_02).exists() is False:
            citation_name_02.save()

        # Here the citation would be "Silva, João C"
        citation_name_03 = CitationName(person_id=person_id, name=last_name+','+' '+first_name_letter_middle_name)
        if CitationName.objects.filter(person_id=person_id, name=citation_name_03).exists() is False:
            citation_name_03.save()

        # Here the last name will be "da Silva"
        if split_name[-2] in prep:
            last_name_with_prep = split_name[-2]+' '+last_name

            # Here the citation would be "da Silva, JC"
            citation_name_prep = CitationName(person_id=person_id, name=last_name_with_prep+','+' '+letters)
            if CitationName.objects.filter(person_id=person_id, name=citation_name_prep).exists() is False:
                citation_name_prep.save()

            # Here the citation would be "da Silva, João Carlos"
            citation_name_prep_02 = CitationName(person_id=person_id, name=last_name_with_prep+','+' '+almost_full_name)
            if CitationName.objects.filter(person_id=person_id, name=citation_name_prep_02).exists() is False:
                citation_name_prep_02.save()

            # Here the citation would be "da Silva, João C"
            citation_name_prep_03 = CitationName(person_id=person_id, name=last_name_with_prep+','+' '+first_name_letter_middle_name)
            if CitationName.objects.filter(person_id=person_id, name=citation_name_prep_03).exists() is False:
                citation_name_prep_03.save()


@login_required
def citation_names(request):
    # Create citation names for each person
    for person in Person.objects.all():
        generate_citation_names(person)

    return render(request, 'admin/index.html')