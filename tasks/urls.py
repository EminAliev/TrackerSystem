from django.conf.urls import url
from django.urls import path

from tasks.views import tasks_render, TaskView, task_create, task_cancel, task_change, definition_create, \
    projects_render, ProjectView, project_create, project_detail, project_cancel, project_change

urlpatterns = [
    path('task_list/', tasks_render, name='task_list'),
    path('task/(?P<pk>\d+)/$', TaskView.as_view(), name='task_view'),
    path('new_task/', task_create, name='task_create'),
    path('^task/(?P<pk>\d+)/cancel/$', task_cancel, name='task_cancel'),
    path('^task/(?P<pk>\d+)/change/$', task_change, name='task_change'),
    path('^task/(?P<pk>\d+)/new_definition/$', definition_create, name='definition_create'),
    path('', projects_render, name='projects_list'),
    path('project/(?P<pk>\d+)/$', project_detail, name='project_view'),
    path('new_project/', project_create, name='project_create'),
    path('^project/(?P<pk>\d+)/cancel/$', project_cancel, name='project_cancel'),
    path('^project/(?P<pk>\d+)/change/$', project_change, name='project_change'),
]
