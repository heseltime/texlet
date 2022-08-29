# Generated by Django 3.2.5 on 2022-08-18 16:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texapp', '0006_remove_letter_formal_bit'),
    ]

    operations = [
        migrations.AddField(
            model_name='letter',
            name='date',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='letter',
            name='enclosed',
            field=models.CharField(blank=True, default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='letter',
            name='ps',
            field=models.CharField(blank=True, default='', max_length=250),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='letter',
            name='reference',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='letter',
            name='salutation',
            field=models.CharField(blank=True, default='Dear ', max_length=50),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='letter',
            name='sign_off',
            field=models.CharField(blank=True, default='Best, ', max_length=50),
            preserve_default=False,
        ),
    ]
