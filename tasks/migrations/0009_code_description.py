# Generated by Django 2.0.10 on 2020-05-15 23:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0008_auto_20200515_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='code',
            name='description',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
