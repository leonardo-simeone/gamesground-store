# Generated by Django 3.2.19 on 2023-07-10 15:20

from django.db import migrations
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='genre',
            field=multiselectfield.db.fields.MultiSelectField(blank=True, choices=[('Action', 'Action'), ('Adventure', 'Adventure'), ('Fantasy', 'Fantasy'), ('Horror', 'Horror'), ('Shooter', 'Shooter'), ('Racing', 'Racing'), ('Rpg', 'Rpg'), ('Sports', 'Sports')], max_length=120, null=True),
        ),
    ]
