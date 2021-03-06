# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-04 22:09
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorimetr', '0016_auto_20190505_0034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='activity',
            field=models.CharField(choices=[('Min', 'Минимальная активность'), ('W', 'Слабая активность'), ('Med', 'Средняя активность'), ('H', 'Высокая активность'), ('E', 'Экстра-активность')], max_length=3),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sex',
            field=models.CharField(choices=[('W', 'Женский'), ('M', 'Мужской')], max_length=1),
        ),
    ]
