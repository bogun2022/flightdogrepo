# Generated by Django 4.1 on 2022-09-12 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_state_category_alter_state_position_source'),
    ]

    operations = [
        migrations.AddField(
            model_name='state',
            name='db_update_num',
            field=models.IntegerField(default=0),
        ),
    ]
