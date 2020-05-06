from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE
from django.urls import reverse

STATUS = (
    ('Новый', 'Новый'),
    ('В процессе', 'В процессе'),
    ('Почти готов', 'Почти готов'),
    ('Готов', 'Готов'),
    ('Отменен', 'Отменен'),
    ('Тестируется', 'Тестируется')
)


class Project(models.Model):
    """Класс модели проекта"""
    title = models.CharField(max_length=150, verbose_name='Название проекта')
    user = models.ForeignKey(User, on_delete=CASCADE, verbose_name='Автор проекта')

    # date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Проект'
        verbose_name_plural = 'Проекты'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('project_view', args=[str(self.id)])


class Task(models.Model):
    """Класс модели задачи"""
    problem = models.TextField(verbose_name='Проблема')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, verbose_name='Проект')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_lead", verbose_name='Автор задачи')
    status = models.CharField(max_length=30, choices=STATUS, verbose_name='Статус задачи')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_worker",
                              verbose_name='Исполнитель задачи')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return self.problem

    def get_absolute_url(self):
        return reverse('task_view', args=[str(self.id)])


class Definition(models.Model):
    """Класс модели коммментарии"""
    definition = models.TextField(verbose_name='Комментарий')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, verbose_name='Задача')
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор комментария')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.definition
