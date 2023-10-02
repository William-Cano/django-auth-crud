from django import forms
from .models import Task

class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'important']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control','placeholder':'Escriba un titulo'}),
            'description': forms.Textarea(attrs={'class': 'form-control','placeholder':'Escriba una descripción'}),
            'important': forms.CheckboxInput(attrs={'class': 'form-check-input'})
        }
