# Generated by Django 3.1.2 on 2020-10-08 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet', '0003_auto_20201007_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='wallet',
            name='balance',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
