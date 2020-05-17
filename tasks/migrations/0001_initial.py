# Generated by Django 2.1.10 on 2020-05-05 16:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Definition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('definition', models.TextField(verbose_name='Комментарий')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор комментария')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150, verbose_name='Название проекта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Автор проекта')),
            ],
            options={
                'verbose_name': 'Проект',
                'verbose_name_plural': 'Проекты',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('problem', models.TextField(verbose_name='Проблема')),
                ('status', models.CharField(choices=[('Новый', 'Новый'), ('В процессе', 'В процессе'), ('Почти готов', 'Почти готов'), ('Готов', 'Готов'), ('Отменен', 'Отменен'), ('Тестируется', 'Тестируется')], max_length=30, verbose_name='Статус задачи')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='owner_worker', to=settings.AUTH_USER_MODEL, verbose_name='Исполнитель задачи')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Project', verbose_name='Проект')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_lead', to=settings.AUTH_USER_MODEL, verbose_name='Автор задачи')),
            ],
            options={
                'verbose_name': 'Задачи',
            },
        ),
        migrations.AddField(
            model_name='definition',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tasks.Task', verbose_name='Задача'),
        ),
    ]