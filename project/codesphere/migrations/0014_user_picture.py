# Generated by Django 2.2.24 on 2022-02-07 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesphere', '0013_remove_user_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='picture',
            field=models.TextField(default='/media/profile/default.png'),
        ),
    ]
