# Generated by Django 3.2.5 on 2022-08-18 10:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('texapp', '0005_auto_20220818_1245'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='formal_bit',
        ),
    ]
