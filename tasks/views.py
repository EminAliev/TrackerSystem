from django.http import HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.views.generic import DetailView

from tasks.forms import FilterForm, TaskForm
from tasks.models import Task


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
            return render(request, "list.html", {'list': tasks_objects, 'form': filter_form})


class TaskView(DetailView):
    model = Task
    template_name = 'task_in.html'


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
        return render(request, "task_create.html", {'form': task_form})
    elif request.method == 'POST':
        task_form = TaskForm(request.POST)
        if task_form.is_valid():
            task_form.save()
        return redirect('task_list')
    return HttpResponseNotAllowed(['POST', 'GET'])
