# Generated by Django 2.2.24 on 2022-01-07 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesphere', '0003_auto_20220107_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(null=True),
        ),
    ]
