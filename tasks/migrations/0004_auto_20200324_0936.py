# Generated by Django 3.0.4 on 2020-03-24 09:36

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20200324_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='label',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='project',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='section',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
        migrations.AddField(
            model_name='task',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
