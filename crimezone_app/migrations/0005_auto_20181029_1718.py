# Generated by Django 2.1.1 on 2018-10-29 17:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crimezone_app', '0004_comment_reply'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reply',
            old_name='post',
            new_name='comment',
        ),
    ]
