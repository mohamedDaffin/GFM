# Generated by Django 5.0.6 on 2024-11-25 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('animaleapp', '0003_animal_nombre_alter_nourriture_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='animal',
            name='nombre',
        ),
        migrations.AddField(
            model_name='typeanimal',
            name='nombre',
            field=models.IntegerField(default=0),
        ),
    ]
