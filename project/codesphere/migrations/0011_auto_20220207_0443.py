# Generated by Django 2.2.24 on 2022-02-07 04:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesphere', '0010_auto_20220117_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.TextField(default='profile/default.png'),
        ),
    ]
