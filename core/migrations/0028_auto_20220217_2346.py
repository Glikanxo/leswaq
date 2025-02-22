# Generated by Django 2.2 on 2022-02-17 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0027_conseil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='annonce',
            name='notice',
        ),
        migrations.AddField(
            model_name='annonce',
            name='deplacement',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='annonce',
            name='echange',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='annonce',
            name='livraison',
            field=models.BooleanField(default=False),
        ),
    ]
