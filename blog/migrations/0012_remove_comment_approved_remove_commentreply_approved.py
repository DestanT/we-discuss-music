# Generated by Django 4.2.3 on 2023-10-30 16:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0011_season_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='approved',
        ),
        migrations.RemoveField(
            model_name='commentreply',
            name='approved',
        ),
    ]