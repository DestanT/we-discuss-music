# Generated by Django 4.2.3 on 2023-10-25 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_rename_body_comment_comment_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='comment',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='commentreplies',
            old_name='reply',
            new_name='body',
        ),
    ]
