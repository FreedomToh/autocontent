# Generated by Django 4.2.4 on 2023-08-19 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='YandexTokenModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.TextField()),
                ('exp_date', models.DateTimeField()),
            ],
        ),
    ]