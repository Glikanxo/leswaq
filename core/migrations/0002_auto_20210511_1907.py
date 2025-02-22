# Generated by Django 2.2 on 2021-05-11 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='annonce',
            old_name='image',
            new_name='img1',
        ),
        migrations.AddField(
            model_name='annonce',
            name='img2',
            field=models.ImageField(default='', upload_to='useruploads'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='annonce',
            name='img3',
            field=models.ImageField(default='', upload_to='useruploads'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='annonce',
            name='img4',
            field=models.ImageField(default='', upload_to='useruploads'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='annonce',
            name='img5',
            field=models.ImageField(default='', upload_to='useruploads'),
            preserve_default=False,
        ),
    ]
