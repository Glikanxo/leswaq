# Generated by Django 2.2 on 2021-05-13 00:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_subscriptions'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='profile_pic',
            field=models.ImageField(default='', upload_to='profile_pics'),
            preserve_default=False,
        ),
    ]
