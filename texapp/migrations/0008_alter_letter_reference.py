# Generated by Django 3.2.5 on 2022-08-19 17:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texapp', '0007_auto_20220818_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='letter',
            name='reference',
            field=models.CharField(max_length=100),
        ),
    ]
