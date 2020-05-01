from django.urls import path

from tasks.views import tasks_render, TaskView, task_create, task_cancel, task_change

urlpatterns = [
    path('list/', tasks_render, name='task_list'),
    path('task/(?P<pk>\d+)/$', TaskView.as_view(), name='task_view'),
    path('new_task/', task_create, name='task_create'),
    path('^task/(?P<pk>\d+)/cancel/$', task_cancel, name='task_cancel'),
    path('^task/(?P<pk>\d+)/change/$', task_change, name='task_change'),
]
