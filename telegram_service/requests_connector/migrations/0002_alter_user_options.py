# Generated by Django 4.2.3 on 2023-07-29 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('requests_connector', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'managed': False, 'ordering': ('-created_at',)},
        ),
    ]
