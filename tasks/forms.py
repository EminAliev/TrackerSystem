from django.forms import ModelForm, Form
from django import forms

from tasks.models import Task, Project, User, Definition, Code, SolveProblem


class FilterForm(Form):
    """Форма фильтрации задач"""
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
    """Форма создания задачи"""

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
    """Форма изменения задачи"""

    class Meta:
        model = Task
        fields = ['status', 'owner']
        labels = {
            'status': 'Статус',
            'owner': 'Исполнитель'
        }


class DefinitionForm(ModelForm):
    """Форма создания комментария к задаче"""

    class Meta:
        model = Definition
        fields = ['definition', 'owner']
        labels = {
            'definition': 'Комментарий',
            'owner': 'Исполнитель'
        }


class ProjectForm(ModelForm):
    """Форма создания проекта"""

    class Meta:
        model = Project
        fields = ['title', 'user']
        labels = {
            'title': 'Название',
            'user': 'Автор'
        }


class ProjectChangeForm(ModelForm):
    """Форма изменения проекта"""

    class Meta:
        model = Project
        fields = ['title']
        labels = {
            'title': 'Название',
        }


class ProblemForm(ModelForm):
    code = forms.CharField(label='Код', required=True, widget=forms.Textarea(attrs={'class': 'form-control'}))

    class Meta:
        model = Code
        fields = ['name_problem', 'description', 'code', 'task']
        labels = {
            'name_problem': 'Название проблемы',
            'description': 'Описание проблемы',
            'task': 'Задание'
        }


class ProblemSolveForm(ModelForm):
    class Meta:
        model = SolveProblem
        fields = ['text']
        labels = {
            'text': 'Решение'
        }
