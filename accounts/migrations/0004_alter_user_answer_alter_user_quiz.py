# Generated by Django 4.1 on 2022-08-03 18:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_answer_alter_user_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='answer',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='user',
            name='quiz',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='qz', to='accounts.quiz'),
        ),
    ]
