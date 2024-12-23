# Generated by Django 5.0.6 on 2024-11-25 16:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animaleapp', '0002_alter_animal_date_enregistrer'),
    ]

    operations = [
        migrations.AddField(
            model_name='animal',
            name='nombre',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='nourriture',
            name='Type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='animaleapp.typeanimal', verbose_name='name_type'),
        ),
    ]
