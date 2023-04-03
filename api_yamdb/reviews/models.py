from django.core.validators import MaxValueValidator, MinValueValidator
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

class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    #author = models.ForeignKey(
        #User,
        #verbose_name='Автор',
        #on_delete=models.CASCADE,
        #related_name='reviews'
    #)
    score = models.PositiveSmallIntegerField(
        verbose_name='Рейтинг',
        validators=[
            MinValueValidator(1, 'Допустимы значения от 1 до 10'),
            MaxValueValidator(10, 'Допустимы значения от 1 до 10')
        ]
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ['pub_date']
        constraints = [
            models.UniqueConstraint(
                fields=['title', 'author'],
                name='unique_review'
            ),
        ]

class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    #author = models.ForeignKey(
        #User,
        #verbose_name='Пользователь',
        #on_delete=models.CASCADE,
        #related_name='comments'
    #)
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']
