# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2019-05-13 14:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('calorimetr', '0021_eating_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Portion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('val', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='dish',
            name='portion',
        ),
        migrations.AddField(
            model_name='portion',
            name='dish',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorimetr.Dish'),
        ),
        migrations.AddField(
            model_name='portion',
            name='eating',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='calorimetr.Eating'),
        ),
    ]