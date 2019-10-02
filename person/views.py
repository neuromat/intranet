# -*- coding: utf-8 -*-
from collections import Counter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import render, redirect
from django.utils.translation import ugettext_lazy as _

from person.models import CitationName, Person

prep = ['e', 'da', 'do', 'de', 'dos', 'E', 'Da', 'Do', 'De', 'Dos']


def name_with_first_letters(names, with_prep):
    letters = ''
    last_name = names[-1]
    last_name_with_prep = names[-2]+' '+last_name

    for name in names:
        if name != last_name and name not in prep:
            letters += name[0]

    if not with_prep:
        return last_name+','+' '+letters
    else:
        return last_name_with_prep+','+' '+letters


def names_without_last_name(names, with_prep):
    last_name = names[-1]
    last_name_with_prep = names[-2]+' '+last_name
    citation_name = [name for name in names if name != last_name and name not in prep]
    citation_name = ' '.join(citation_name)

    if not with_prep:
        return last_name+','+' '+citation_name

    else:
        return last_name_with_prep+','+' '+citation_name


def first_name_and_first_letter(names, with_prep):
    first_letter = ''
    first_name = names[0]
    last_name = names[-1]
    last_name_with_prep = names[-2]+' '+last_name

    for name in names:
        if name != first_name and name != last_name and name not in prep:
            first_letter += name[0]

    if not with_prep:
        if first_letter != '':
            citation_name = first_name+' '+first_letter
            return last_name+','+' '+citation_name
        else:
            citation_name = first_name
            return last_name+','+' '+citation_name

    else:
        if first_letter != '':
            citation_name = first_name+' '+first_letter
            return last_name_with_prep+','+' '+citation_name
        else:
            citation_name = first_name
            return last_name_with_prep+','+' '+citation_name


def generate_citation_names(person):

    # Get full name and id from person.
    full_name = person.full_name
    person_id = person.pk

    # Split the full name.
    split_name = full_name.split()

    # Maybe the user has a default citation
    citation_default = CitationName.objects.filter(person_id=person_id, default_name=True)

    # Get the first letter of the name except the last name
    # letters = name_with_first_letters(split_name)
    citation_01 = name_with_first_letters(split_name, False)

    # Get names without last name
    # almost_full_name = names_without_last_name(split_name)
    citation_02 = names_without_last_name(split_name, False)

    # Get first name and first letter of the middle name
    # first_name_letter_middle_name = first_name_and_first_letter(split_name)
    citation_03 = first_name_and_first_letter(split_name, False)

    # Imagine a person called João Carlos da Silva.
    # Here the citation would be "Silva, JC"
    if citation_default:
        CitationName.objects.get_or_create(person_id=person_id, name=citation_01)
    else:
        CitationName.objects.get_or_create(person_id=person_id, name=citation_01, default_name=True)

    # Here the citation would be "Silva, João Carlos"
    CitationName.objects.get_or_create(person_id=person_id, name=citation_02)

    # Here the citation would be "Silva, João C"
    CitationName.objects.get_or_create(person_id=person_id, name=citation_03)

    # Here the last name will be "da Silva"
    if split_name[-2] in prep:

        # last_name_with_prep = split_name[-2]+' '+last_name
        prep_01 = name_with_first_letters(split_name, True)
        prep_02 = names_without_last_name(split_name, True)
        prep_03 = first_name_and_first_letter(split_name, True)

        # Here the citation would be "da Silva, JC"
        CitationName.objects.get_or_create(person_id=person_id, name=prep_01)

        # Here the citation would be "da Silva, João Carlos"
        CitationName.objects.get_or_create(person_id=person_id, name=prep_02)

        # Here the citation would be "da Silva, João C"
        CitationName.objects.get_or_create(person_id=person_id, name=prep_03)


@login_required
def citation_names(request):
    # Create citation names for each person
    for person in Person.objects.all():
        generate_citation_names(person)

    messages.success(request, _('Successfully updated citation names.'))
    return redirect(reverse('admin:index'))


@login_required
def researchers(request):
    list_of_researchers = Person.objects.all()
    list_of_roles = []
    for research in list_of_researchers:
        list_of_roles.append(str(research.role))
    table_of_roles = (Counter(list_of_roles)).items()
    context = {'list_of_researchers': list_of_researchers, 'table_of_roles': table_of_roles}
    return render(request, 'report/person/researchers.html', context)
