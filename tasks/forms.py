from django.forms import ModelForm, Form
from django import forms

from tasks.models import Task, Project, User


class FilterForm(Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False)
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    owner = forms.ModelChoiceField(User.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        ('New', 'New'),
        ('In progress', 'In progress'),
        ('Ready', 'Ready'),
        ('Completed', 'Completed'),
        ('Canceled', 'Canceled'),
        ('Being tested', 'Being tested'),
        (None, '------')), required=False)
    search = forms.CharField(max_length=150, required=False)
