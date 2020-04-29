from django.urls import path

from tasks.views import tasks_render, TaskView, task_create, task_cancel

urlpatterns = [
    path('list/', tasks_render, name='task_list'),
    path('task/(?P<pk>\d+)/$', TaskView.as_view(), name='task_view'),
    path('new_task/', task_create, name='task_create'),
    path('^task/(?P<pk>\d+)/delete/$', task_cancel, name='task_cancel')
]
