# Generated by Django 3.1.7 on 2021-04-06 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_service', '0005_auto_20210406_1755'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='name',
            field=models.CharField(default='', max_length=255, verbose_name='Name'),
        ),
    ]
