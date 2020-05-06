from django.contrib.auth.models import User
from django.db import models


class Chat(models.Model):
    """Класс модели чата"""
    users = models.ManyToManyField(User, verbose_name="Пользователи")

    def __str__(self):
        return self.users

    class Meta:
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'


class Message(models.Model):
    """Класс модели сообщений"""
    chat = models.ForeignKey(Chat, related_name='messages', on_delete=models.CASCADE, verbose_name='Чат')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Отправитель')
    date = models.DateTimeField(auto_now=True, verbose_name='Дата отправления')
    read = models.BooleanField(default=False, verbose_name='Прочитано')
    text = models.TextField(null=False, blank=False, default=None, verbose_name='Текст сообщения')

    def __str__(self):
        return self.chat

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'
