# Generated by Django 3.2 on 2023-03-30 06:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0001_create_primary_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Жанр')),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
        migrations.AddField(
            model_name='title',
            name='rating',
            field=models.IntegerField(default=0, verbose_name='Рейтинг'),
        ),
        migrations.CreateModel(
            name='GenreTitle',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genre_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.genre')),
                ('title_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='reviews.title')),
            ],
        ),
        migrations.AddField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(through='reviews.GenreTitle', to='reviews.Genre'),
        ),
    ]
