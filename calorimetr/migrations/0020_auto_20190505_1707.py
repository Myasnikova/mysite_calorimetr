# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-05 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('calorimetr', '0019_userprofile_wish_weight'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userweight',
            name='date',
            field=models.DateField(),
        ),
    ]
