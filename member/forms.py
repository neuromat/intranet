from django import forms
from member.models import ProjectMember, Other
from cep.widgets import CEPInput


class ProjectMemberForm(forms.ModelForm):

    class Meta:
        model = ProjectMember

        fields = ['zipcode', 'street', 'district', 'city', 'state']

        widgets = {
            'zipcode': CEPInput(address={'street': 'id_street', 'district': 'id_district', 'city': 'id_city',
                                         'state': 'id_state'}, attrs={'pattern': '\d{5}-?\d{3}'}),
        }


class OtherForm(forms.ModelForm):

    class Meta:
        model = Other

        fields = ['zipcode', 'street', 'district', 'city', 'state']

        widgets = {
            'zipcode': CEPInput(address={'street': 'id_street', 'district': 'id_district', 'city': 'id_city',
                                         'state': 'id_state'}, attrs={'pattern': '\d{5}-?\d{3}'}),
        }
