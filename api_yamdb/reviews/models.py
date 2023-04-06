from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from users.models import User


class Category(models.Model):
    name = models.CharField('Категория', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Жанр', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название', max_length=256)
    year = models.PositiveIntegerField('Год выпуска', db_index=True)
    rating = models.IntegerField('Рейтинг', default=None, blank=True,
                                 null=True)
    description = models.TextField('Описание', blank=True, null=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )
    genre = models.ManyToManyField(Genre, through='GenreTitle')

    class Meta:
        ordering = ['-id']
    
    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    title_id = models.ForeignKey(Title, on_delete=models.CASCADE)
    genre_id = models.ForeignKey(Genre, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f'{self.title_id} {self.genre_id}'


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='reviews',
        db_index=True
    )
    score = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Рейтинг',
        validators=[MinValueValidator(1), MaxValueValidator(10)],
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

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    text = models.TextField(
        verbose_name='Текст',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='comments',
        db_index=True
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['pub_date']

    def __str__(self):
        return self.text
