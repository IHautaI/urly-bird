# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('urlyapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255)),
                ('description', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='bookmark',
            name='profile',
            field=models.ForeignKey(to='urlyapp.Profile', null=True),
        ),
    ]
