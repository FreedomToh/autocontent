# Generated by Django 4.0.10 on 2023-07-21 15:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0015_delete_requeststatusesmodel_delete_statusesmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='StatusesModel',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'statuses',
            },
        ),
        migrations.CreateModel(
            name='RequestStatusesModel',
            fields=[
                ('request_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='api.requestsmodel')),
                ('audio_status', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='audio_status', to='api.statusesmodel')),
                ('gpt_status', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='gpt_status', to='api.statusesmodel')),
                ('video_status', models.ForeignKey(default=0, on_delete=django.db.models.deletion.DO_NOTHING, related_name='video_status', to='api.statusesmodel')),
            ],
            options={
                'db_table': 'requests_status',
            },
        ),
    ]
