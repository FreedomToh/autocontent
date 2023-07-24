# Generated by Django 4.0.10 on 2023-07-23 10:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_remove_requeststatusesmodel_audio_status_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='RequestsModel',
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
