from django.test import TestCase
from models import AcademicWork, TypeAcademicWork, Person
from views import academic_works


def create_academic_work_mock():
    academic_work = TypeAcademicWork.objects.create(name='postdoc')
    academic_work.save()

    advisee = Person.objects.create(full_name='John Smith')
    advisee.save()

    advisor = Person.objects.create(full_name='Emma Miller')
    advisor.save()

    mock = AcademicWork()
    mock.type = academic_work
    mock.advisee = advisee
    mock.advisor = advisor
    mock.schollarship = 'FAPESP - Proc. 2014/07254-0'
    mock.save()
    return mock


class ResearchValidation(TestCase):
    postdoc_01 = {}
    postdoc_02 = {}
    util = create_academic_work_mock()

    def setUp(self):
        self.postdoc_01 = {'title': 'Postdoc 01',
                           'start_date': '20/08/2013',
                           'end_date': '26/08/2014'
                           }

        self.postdoc_02 = {'title': 'Postdoc 02',
                           'start_date': '01/06/2013',
                           'end_date': '30/06/2014'
                           }


def test_current_report(self):
    start_date_report = '01/07/2014'
    end_date_report = '31/07/2015'

    response = self.client.post(academic_works)
