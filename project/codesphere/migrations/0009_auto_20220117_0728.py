# Generated by Django 2.2.24 on 2022-01-17 07:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codesphere', '0008_user_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='picture',
            field=models.ImageField(default='profile/ccf4eec2c210e6f03da4edc949f6b4f6_MK5duyy.jpg', upload_to='profile/'),
        ),
    ]
