# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('urlyapp', '0004_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.AddField(
            model_name='bookmark',
            name='short',
            field=models.URLField(null=True),
        ),
        migrations.AddField(
            model_name='click',
            name='bookmark',
            field=models.ForeignKey(to='urlyapp.Bookmark'),
        ),
        migrations.AddField(
            model_name='click',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
