# Generated by Django 3.1.5 on 2021-02-08 10:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('address_regions', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='region',
            options={'ordering': ('country_area', 'city', 'city_area')},
        ),
        migrations.RenameField(
            model_name='region',
            old_name='district',
            new_name='city_area',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='province',
            new_name='country_area',
        ),
        migrations.RenameField(
            model_name='region',
            old_name='zipcode',
            new_name='postal_code',
        ),
    ]
