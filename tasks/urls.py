from django.urls import path

from tasks.views import tasks_render, TaskView, task_create, task_cancel, task_change, definition_create, \
    projects_render, ProjectView

urlpatterns = [
    path('task_list/', tasks_render, name='task_list'),
    path('task/(?P<pk>\d+)/$', TaskView.as_view(), name='task_view'),
    path('new_task/', task_create, name='task_create'),
    path('^task/(?P<pk>\d+)/cancel/$', task_cancel, name='task_cancel'),
    path('^task/(?P<pk>\d+)/change/$', task_change, name='task_change'),
    path('^task/(?P<pk>\d+)/new_definition/$', definition_create, name='definition_create'),
    path('project_list/', projects_render, name='projects_list'),
    path('project/(?P<pk>\d+)/$', ProjectView.as_view(), name='project_view'),
]
