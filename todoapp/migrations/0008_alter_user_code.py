# Generated by Django 4.2.13 on 2024-07-07 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todoapp', '0007_todoitems_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='code',
            field=models.CharField(max_length=8),
        ),
    ]
