# Generated by Django 2.2 on 2021-06-22 02:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_annonce_categorie'),
    ]

    operations = [
        migrations.AlterField(
            model_name='annonce',
            name='categorie',
            field=models.CharField(choices=[('Téléphones', 'Téléphones'), ('Véhicules', 'Véhicules'), ('Immobilier', 'Immobilier'), ('Electronique & Electroménager', 'Electronique & Electroménager'), ('Emploi', 'Emploi'), ('Informatique', 'Informatique'), ('Mode & Beauté', 'Mode & Beauté'), ('Maison & Fournitures', 'Maison & Fournitures'), ('Loisirs & Divertissements', 'Loisirs & Divertissements'), ('Matériaux & Equipement', 'Matériaux & Equipement'), ('Voyages', 'Voyages'), ('Services', 'Services'), ('Divers', 'Divers')], max_length=256),
        ),
    ]
