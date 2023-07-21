# Generated by Django 4.0.10 on 2023-07-21 14:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_rename_requests_requestsmodel'),
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
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('audio_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='audio_status', to='api.statusesmodel')),
                ('gpt_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='gpt_status', to='api.statusesmodel')),
                ('request_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.requestsmodel')),
                ('video_status', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='video_status', to='api.statusesmodel')),
            ],
            options={
                'db_table': 'requests_status',
            },
        ),
    ]
