# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-04 12:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorimetr', '0010_auto_20190504_1523'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dish',
            name='calorie',
        ),
        migrations.AddField(
            model_name='dish',
            name='portion',
            field=models.IntegerField(default=0),
        ),
    ]
