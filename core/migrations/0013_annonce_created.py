# Generated by Django 2.2 on 2021-10-25 22:21

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210708_0115'),
    ]

    operations = [
        migrations.AddField(
            model_name='annonce',
            name='created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
