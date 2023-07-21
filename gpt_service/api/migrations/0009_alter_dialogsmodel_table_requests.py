# Generated by Django 4.0.10 on 2023-07-21 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_alter_dialogsmodel_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='dialogsmodel',
            table='gpt_dialogs',
        ),
        migrations.CreateModel(
            name='Requests',
            fields=[
                ('request_id', models.AutoField(primary_key=True, serialize=False)),
                ('request_src', models.CharField(max_length=255)),
                ('request_text', models.TextField(blank=True, null=True)),
                ('response_text', models.TextField(blank=True, null=True)),
                ('audio_url', models.TextField(blank=True, null=True)),
                ('video_url', models.TextField(blank=True, null=True)),
                ('finished', models.BooleanField(default=False)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='api.user')),
            ],
            options={
                'db_table': 'gpt_requests',
            },
        ),
    ]
