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


class User(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=150)
    user = models.ForeignKey(User, on_delete=CASCADE)

    def __str__(self):
        return self.title


class Task(models.Model):
    problem = models.TextField()
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="team_lead")
    status = models.CharField(max_length=30, choices=STATUS)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner_worker")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.problem

    def get_absolute_url(self):
        return reverse('task_view', args=[str(self.id)])


class Definition(models.Model):
    definition = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.definition
