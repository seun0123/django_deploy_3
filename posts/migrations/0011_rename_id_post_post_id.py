# Generated by Django 3.2.6 on 2022-08-15 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_auto_20220816_0456'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='id',
            new_name='post_id',
        ),
    ]
