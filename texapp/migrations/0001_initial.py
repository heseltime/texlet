# Generated by Django 3.2.5 on 2022-08-17 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Letter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('addresse_first_name', models.CharField(max_length=20)),
                ('addresse_last_name', models.CharField(max_length=50)),
                ('addresse_street_address', models.CharField(max_length=50)),
                ('addresse_street_number', models.IntegerField()),
                ('addresse_zip_code', models.IntegerField()),
                ('addresse_city', models.CharField(max_length=50)),
                ('salutation', models.CharField(max_length=50)),
                ('paragraph', models.CharField(max_length=250)),
                ('sign_off', models.CharField(max_length=50)),
            ],
        ),
    ]
