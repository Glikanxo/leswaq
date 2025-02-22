# Generated by Django 2.2 on 2021-10-22 00:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'ordering': ['-last_message_time']},
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AddField(
            model_name='chat',
            name='last_message_time',
            field=models.DateTimeField(null=True),
        ),
    ]
