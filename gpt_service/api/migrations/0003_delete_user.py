# Generated by Django 4.0.10 on 2023-07-18 14:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_user_table'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User',
        ),
    ]