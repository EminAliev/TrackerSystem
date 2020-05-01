from django.forms import ModelForm, Form
from django import forms

from tasks.models import Task, Project, User, Definition


class FilterForm(Form):
    project = forms.ModelChoiceField(Project.objects.all(), required=False, label='Проект')
    user = forms.ModelChoiceField(User.objects.all(), required=False, label='Автор')
    owner = forms.ModelChoiceField(User.objects.all(), required=False, label='Исполнитель')
    status = forms.ChoiceField(choices=(
        ('Новый', 'Новый'),
        ('В процессе', 'В процессе'),
        ('Почти готов', 'Почти готов'),
        ('Готов', 'Готов'),
        ('Отменен', 'Отменен'),
        ('Тестируется', 'Тестируется'),
        (None, '------')), required=False, label='Статус')
    search = forms.CharField(max_length=150, required=False, label='Поиск')


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


class TaskChangeForm(ModelForm):
    class Meta:
        model = Task
        fields = ['status', 'owner']
        labels = {
            'status': 'Статус',
            'owner': 'Исполнитель'
        }


class DefinitionForm(ModelForm):
    class Meta:
        model = Definition
        fields = ['definition', 'owner']
        labels = {
            'definition': 'Комментарий',
            'owner': 'Исполнитель'
        }
