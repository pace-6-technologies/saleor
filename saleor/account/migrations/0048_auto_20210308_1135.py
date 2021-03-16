# Generated by Django 3.1.7 on 2021-03-08 11:35

import django.contrib.postgres.indexes
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0047_auto_20200810_1415"),
    ]

    operations = [
        migrations.AddIndex(
            model_name="user",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["private_metadata"], name="user_p_meta_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="user",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["metadata"], name="user_meta_idx"
            ),
        ),
    ]
