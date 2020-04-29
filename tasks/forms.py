from django.forms import ModelForm, Form
from django import forms

from tasks.models import Task, Project, User


class FilterForm(Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False)
    user = forms.ModelChoiceField(User.objects.all(), required=False)
    owner = forms.ModelChoiceField(User.objects.all(), required=False)
    status = forms.ChoiceField(choices=(
        ('Новый', 'Новый'),
        ('В процессе', 'В процессе'),
        ('Почти готов', 'Почти готов'),
        ('Готов', 'Готов'),
        ('Отменен', 'Отменен'),
        ('Тестируется', 'Тестируется'),
        (None, '------')), required=False)
    search = forms.CharField(max_length=150, required=False)


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['problem', 'project', 'status', 'user', 'owner']
        labels = {
            'problem': 'Проблема',
            'project': 'Проект',
            'status': 'Текущий статус',
            'user': 'Автор задачи',
            'owner': 'Работник, который должен выполнить',
        }
