# Generated by Django 2.0.10 on 2020-05-15 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='name_problem',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]