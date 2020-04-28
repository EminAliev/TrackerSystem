from django.urls import path

from tasks.views import tasks_render, TaskView

urlpatterns = [
    path('list/', tasks_render, name='task_list'),
    path('task/(?P<pk>\d+)/$', TaskView.as_view(), name='task_view')
]
