from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import send_mail
from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, ListView

from tasks.forms import FilterForm, TaskForm, TaskChangeForm, DefinitionForm, ProjectForm, ProjectChangeForm, \
    ProblemForm, ProblemSolveForm
from tasks.models import Task, Definition, Project, Code, SolveProblem


@login_required
def tasks_render(request):
    """Просмотр задач и их фильтрация"""
    if request.method == "GET":
        tasks_objects = Task.objects.all()
        filter_form = FilterForm(request.GET)
        if filter_form.is_valid():
            tasks_objects = task_filter(project=filter_form.cleaned_data['project'],
                                        user=filter_form.cleaned_data['user'],
                                        owner=filter_form.cleaned_data['owner'],
                                        status=filter_form.cleaned_data['status'],
                                        search=filter_form.cleaned_data['search']
                                        )
            return render(request, "tasks/list.html", {'list': tasks_objects, 'form': filter_form})


class TaskView(LoginRequiredMixin, DetailView):
    """Просмотр конкретной задачи"""
    model = Task
    template_name = 'tasks/task_in.html'

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        definitions = Definition.objects.filter(
            task__id=self.kwargs['pk'])
        problems = Code.objects.filter(
            task__id=self.kwargs['pk'])
        context['definitions'] = definitions
        definition_statistics = definitions_statistics(definitions)
        context['definition_statistics'] = definition_statistics
        context['problems'] = problems
        return context


def definitions_statistics(definitions):
    """Статистика по комментариям, оставленным к задачам"""
    s = {}
    for definition in definitions:
        current_date = definition.date.date().strftime("%Y-%m-%d")
        if current_date in s:
            s[current_date]['d_definitions'] += 1
            s[current_date]['d_owners'].append(definition.owner)
        else:
            s[current_date] = {'d_definitions': 1, 'd_owners': [definition.owner]}
    for current_date in s:
        s[current_date]['d_owners'] = len(set(s[current_date]['d_owners']))
    return s


def task_filter(**kwargs):
    """Фильтрация по признакам"""
    list_tasks = Task.objects.all()
    if kwargs.get('project'):
        list_tasks = list_tasks.filter(project=kwargs.get('project'))
    if kwargs.get('user'):
        list_tasks = list_tasks.filter(user=kwargs.get('user'))
    if kwargs.get('owner'):
        list_tasks = list_tasks.filter(owner=kwargs.get('owner'))
    if kwargs.get('status'):
        list_tasks = list_tasks.filter(status=kwargs.get('status'))
    if kwargs.get('search'):
        list_tasks = list_tasks.filter(problem__icontains=kwargs.get('search'))
    return list_tasks


@login_required
def task_create(request):
    """Создание новой задачи"""
    if request.method == 'GET':
        task_form = TaskForm()
        return render(request, "tasks/task_create.html", {'form': task_form})
    elif request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            cd = task_form.cleaned_data
            task_form.save()
            # при создании новой задаче работнику присылается e-mail письмо с описанием и статусом задачи
            subject = 'Новое задание'
            message = 'Автором {}, была создана новое задание "{}" в проекте "{}", статус задачи "{}, исполнитель задачи "{}"'.format(
                cd['user'],
                cd['problem'],
                cd['project'],
                cd['status'],
                cd['owner'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['owner'].email])
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST', 'GET'])


@login_required
def task_change(request, pk):
    """Изменение задачи"""
    if request.method == 'GET':
        task_form = TaskChangeForm()
        return render(request, 'tasks/task_change.html', {'form': task_form})
    elif request.method == 'POST':
        task_form = TaskChangeForm(request.POST)
        task_object = Task.objects.get(id=pk)
        if task_form.is_valid():
            status_change = task_form.cleaned_data['status']
            owner_change = task_form.cleaned_data['owner']
            task_object.status = status_change
            task_object.worker = owner_change
            cd = task_form.cleaned_data
            task_object.save()
            # при изменении задачи работнику присылается e-mail письмо с измененным статусом задачи
            subject = 'Изменение задачи'
            message = 'Статус задачи был изменен на "{}", исполнитель задачи: "{}"'.format(
                cd['status'],
                cd['owner'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['owner'].email])
        return redirect('task_view', pk=pk)
    return HttpResponseNotAllowed(['POST', 'GET'])


@login_required
def task_cancel(request, pk):
    """Удаление задачи"""
    if request.method == 'DELETE' or request.method == 'POST':
        task = get_object_or_404(Task, id=pk)
        task.delete()
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST'])


@login_required
def definition_create(request, pk):
    """Создание комментария"""
    if request.method == 'GET':
        definition_form = DefinitionForm()
        return render(request, "definitions/definition_create.html", {'form': definition_form})
    elif request.method == 'POST':
        definition_form = DefinitionForm(request.POST)
        task_object = Task.objects.get(id=pk)
        if definition_form.is_valid():
            new_definition = definition_form.cleaned_data['definition']
            owner = definition_form.cleaned_data['owner']
            definition = Definition(definition=new_definition, owner=owner, task=task_object)
            cd = definition_form.cleaned_data
            definition.save()
            # при создания комментария к задаче работнику присылается e-mail письмо
            subject = 'Добавлен комментарий к задаче'
            message = 'Был добавлен комментарий к задаче пользователем "{}"'.format(
                cd['owner'])
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd['owner'].email])
        return redirect(task_object.get_absolute_url())
    return HttpResponseNotAllowed(['POST', 'GET'])


@login_required
def projects_render(request):
    """Просмотр проектов"""
    if request.method == "GET":
        project_objects = Project.objects.all()
        return render(request, "projects/list.html", {'list': project_objects})


class ProjectView(LoginRequiredMixin, DetailView):
    """Просмотр конкретного проекта"""
    model = Project
    template_name = 'projects/project_in.html'


@login_required
def project_create(request):
    """Создание нового проекта"""
    if request.method == 'GET':
        project_form = ProjectForm()
        return render(request, "projects/project_create.html", {'form': project_form})
    elif request.method == 'POST':
        project_form = ProjectForm(request.POST)
        if project_form.is_valid():
            project_form.save()
        return redirect('projects_list')
    return HttpResponseNotAllowed(['POST', 'GET'])


@login_required
def project_detail(request, pk):
    """Просмотр задач, относящихся к конкретному проекту"""
    project = get_object_or_404(Project, id=pk)
    task_object = Task.objects.filter(project__task__project_id=pk).distinct()
    return render(request, 'projects/project_in.html', {'project': project, 'task': task_object})


@login_required
def project_change(request, pk):
    """Изменение проекта"""
    if request.method == 'GET':
        project_form = ProjectChangeForm()
        return render(request, 'projects/project_change.html', {'form': project_form})
    elif request.method == 'POST':
        project_form = ProjectChangeForm(request.POST)
        project_object = Project.objects.get(id=pk)
        if project_form.is_valid():
            title_change = project_form.cleaned_data['title']
            project_object.title = title_change
            project_object.save()
        return redirect('project_view', pk=pk)
    return HttpResponseNotAllowed(['POST', 'GET'])


@login_required
def project_cancel(request, pk):
    """Удаление проекта"""
    if request.method == 'DELETE' or request.method == 'POST':
        project = get_object_or_404(Project, id=pk)
        task_object = Task.objects.filter(project__task__project_id=pk).distinct()
        # definitions_objects = Definition.objects.filter()
        project.delete()
        task_object.delete()
        return redirect('projects_list')
    return HttpResponseNotAllowed(['POST'])


@login_required
def problem_create(request, pk):
    """Создание проблемы, возникающая при выполнении таска"""
    if request.method == 'GET':
        problem_form = ProblemForm()
        return render(request, "problems/problem_task.html", {'form': problem_form})
    elif request.method == 'POST':
        problem_form = ProblemForm(request.POST)
        task_object = Task.objects.get(id=pk)
        if problem_form.is_valid():
            problem_object = Code.objects.create(name_problem=problem_form.cleaned_data['name_problem'],
                                                 code=problem_form.cleaned_data['code'], owner=request.user,
                                                 task=task_object,
                                                 description=problem_form.cleaned_data['description'])
            problem_object.save()
        return redirect(task_object.get_absolute_url())
    return HttpResponseNotAllowed(['POST', 'GET'])


@login_required
def problem_solved(request, pk):
    """Решение проблемы"""
    if request.method == 'GET':
        solve_form = ProblemSolveForm()
        return render(request, "problems/solve.html", {'form': solve_form})
    elif request.method == 'POST':
        solve_form = ProblemSolveForm(request.POST)
        problem = Code.objects.get(id=pk)
        if solve_form.is_valid():
            problem_object = SolveProblem.objects.create(text=solve_form.cleaned_data['text'], owner=request.user,
                                                         problem=problem)
            problem_object.save()
        return redirect('problem_list')
    return HttpResponseNotAllowed(['POST', 'GET'])


class CodeList(LoginRequiredMixin, ListView):
    """Список проблем"""
    model = Code
    template_name = 'problems/list_problems.html'


class SolveProblemList(LoginRequiredMixin, ListView):
    """Список решений"""
    model = SolveProblem
    template_name = 'problems/list_solved_problems.html'
