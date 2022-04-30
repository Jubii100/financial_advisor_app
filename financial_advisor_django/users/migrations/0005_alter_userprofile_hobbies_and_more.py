# Generated by Django 4.0.2 on 2022-04-30 05:33

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_user_profile_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='hobbies',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128, null=True), size=5),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='interests',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=128, null=True), size=5),
        ),
    ]
