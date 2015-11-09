# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Face',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('year', models.IntegerField(default=0)),
                ('stage_num', models.IntegerField(default=0)),
                ('gradient', models.FloatField(default=0)),
                ('img_name', models.CharField(max_length=200)),
            ],
        ),
    ]
