# Generated by Django 2.2.24 on 2022-01-17 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesphere', '0009_auto_20220117_0728'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='profile/default.png', upload_to='profile/'),
        ),
    ]
