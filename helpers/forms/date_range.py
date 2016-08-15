from django import forms

#  Form with jquerys datepicker
DateInput = forms.DateInput(format=['%d-%m-%Y'], attrs={'class': 'datepicker', 'placeholder':'DD/MM/AAAA'})

#  Creates a form that comes with the datepicker widget
class DateRangeForm(forms.Form):
    start_date = forms.DateField(widget=DateInput)
    end_date = forms.DateField(widget=DateInput)
