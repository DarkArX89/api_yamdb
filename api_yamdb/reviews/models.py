from django.db import models


class Category(models.Model):
    name = models.CharField('Категория', max_length=50)
    slug = models.SlugField(unique=True)

class Title(models.Model):
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField('Год выпуска')
    category = models.ForeignKey(
        Category, 
        on_delete=models.SET_NULL,
        related_name='titles',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name