from django import forms

from company.models.title import Title


class TitleForm(forms.ModelForm):
    class Meta:
        model = Title
        fields = '__all__'
