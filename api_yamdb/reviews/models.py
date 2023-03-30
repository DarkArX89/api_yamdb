from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    slug = models.SlugField(unique=True)

    # def __str__(self):
    #     return f'{self.name} {self.slug}'


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=50)
    slug = models.SlugField(unique=True)


class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField('Год выпуска')
    rating = models.IntegerField('Рейтинг', default=0)
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'
