# Generated by Django 4.1 on 2022-08-25 19:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='state',
            old_name='category_id',
            new_name='category',
        ),
        migrations.RenameField(
            model_name='state',
            old_name='position_source_id',
            new_name='position_source',
        ),
    ]