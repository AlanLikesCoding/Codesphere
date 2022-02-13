# Generated by Django 2.2.24 on 2022-02-10 05:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('codesphere', '0015_answercomment_questioncomment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answercomment',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answer_relation', to='codesphere.Answer'),
        ),
        migrations.AlterField(
            model_name='answercomment',
            name='commenter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='answer_commenter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='commenter',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='question_commenter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='questioncomment',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question_relation', to='codesphere.Question'),
        ),
    ]
