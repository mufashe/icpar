from django import forms

from company.models import Department, Title
from leaveMan.models import Leave


class LeaveForm(forms.ModelForm):
    number = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}))
    first_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'readonly': 'True'}))
    last_name = forms.CharField(max_length=250, widget=forms.TextInput(attrs={'readonly': 'True'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(),
                                        widget=forms.Select(attrs={'readonly': 'readonly'}))
    title = forms.ModelChoiceField(queryset=Title.objects.all(), widget=forms.Select(attrs={'readonly': 'readonly'}))
    home_phone = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}))
    mobile_phone = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}))
    home_address = forms.CharField(max_length=150, widget=forms.TextInput(attrs={'readonly': 'True'}))
    birth_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'True'}, ))
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'True'}), label='Hired On')
    inDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date', 'readonly': 'True'}), label='Returning On')
    outDate = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), label='Leaving On')
    leave_days_used = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}), label='Consumed Days')
    # leave_days = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}))
    months_in_institution = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}))
    total_leave_days = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'True'}))

    class Meta:
        model = Leave
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(LeaveForm, self).__init__(*args, **kwargs)
        self.fields['leave_status'].disabled = True
