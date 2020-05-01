from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView

from tasks.forms import FilterForm, TaskForm, TaskChangeForm, DefinitionForm
from tasks.models import Task, Definition


def tasks_render(request):
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


class TaskView(DetailView):
    model = Task
    template_name = 'tasks/task_in.html'

    def get_context_data(self, **kwargs):
        context = super(TaskView, self).get_context_data(**kwargs)
        definitions = Definition.objects.filter(
            task__id=self.kwargs['pk'])
        context['definitions'] = definitions
        definition_statistics = definitions_statistics(definitions)
        context['definition_statistics'] = definition_statistics
        return context


def definitions_statistics(definitions):
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


def task_create(request):
    if request.method == 'GET':
        task_form = TaskForm()
        return render(request, "tasks/task_create.html", {'form': task_form})
    elif request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST', 'GET'])


def task_change(request, pk):
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
            task_object.save()
        return redirect('task_view', pk=pk)
    return HttpResponseNotAllowed(['POST', 'GET'])


def task_cancel(request, pk):
    if request.method == 'DELETE' or request.method == 'POST':
        task = get_object_or_404(Task, id=pk)
        task.delete()
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST'])


def definition_create(request, pk):
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
            definition.save()
        return redirect(task_object.get_absolute_url())
    return HttpResponseNotAllowed(['POST', 'GET'])
