# Generated by Django 3.2.5 on 2022-08-17 21:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('texapp', '0002_letter_enclosed'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letter',
            name='addresse_city',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='addresse_first_name',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='addresse_last_name',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='addresse_street_address',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='addresse_street_number',
        ),
        migrations.RemoveField(
            model_name='letter',
            name='addresse_zip_code',
        ),
        migrations.AddField(
            model_name='letter',
            name='formal_bit',
            field=models.BooleanField(default=False, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='letter',
            name='ps',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='letter',
            name='reference',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='letter',
            name='reference_bit',
            field=models.BooleanField(default=False, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='letter',
            name='salutation',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='letter',
            name='sign_off',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
