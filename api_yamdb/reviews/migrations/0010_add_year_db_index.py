# Generated by Django 3.2 on 2023-04-06 05:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0009_year_type_field'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='year',
            field=models.PositiveIntegerField(db_index=True, verbose_name='Год выпуска'),
        ),
    ]