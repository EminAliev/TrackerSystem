# Generated by Django 2.0.10 on 2020-05-15 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0010_solveproblem'),
    ]

    operations = [
        migrations.RenameField(
            model_name='code',
            old_name='text',
            new_name='code',
        ),
    ]