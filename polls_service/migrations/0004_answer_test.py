# Generated by Django 3.1.7 on 2021-04-12 11:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('polls_service', '0003_test'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='test',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='polls_service.test'),
            preserve_default=False,
        ),
    ]
