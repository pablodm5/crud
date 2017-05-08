from django import forms
from .models import Course

class CourseForm(forms.ModelForm):

    class Meta:
        model=Course
        fields=[
        'name',
        'start_date',
        'end_date',
        'picture',
        ]
        labels={
        'name':'Nombre',
        'start_date':'Fecha de inicio',
        'end_date':'Fecha final',
        'picture':'Imagen',
        }
        widgets={
        'name':forms.TextInput(attrs={'class':'form-control'}),
        'start_date':forms.TextInput(attrs={'class':'form-control datepicker'}),
        'end_date':forms.TextInput(attrs={'class':'form-control datepicker'}),
        }
