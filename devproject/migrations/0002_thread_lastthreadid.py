# Generated by Django 2.2 on 2019-04-08 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devproject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='thread',
            name='lastthreadid',
            field=models.IntegerField(default=0, verbose_name='向下'),
        ),
    ]
