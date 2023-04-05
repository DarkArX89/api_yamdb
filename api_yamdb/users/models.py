from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.db import models


USER = 'user'
ADMIN = 'admin'
MODERATOR = 'moderator'

REGEX = r'^[\w.@+-]+\Z'


class User(AbstractUser):
    USER_ROLES = [
        (USER, 'user'),
        (ADMIN, 'administrator'),
        (MODERATOR, 'moderator'),
    ]

    username = models.CharField(max_length=150,
                                unique=True, blank=False,
                                null=False,
                                verbose_name='Имя для входа',
                                validators=[RegexValidator(REGEX)])
    email = models.EmailField(max_length=254,
                              unique=True,
                              blank=False,
                              null=False,
                              verbose_name='Почта')
    first_name = models.CharField(max_length=150,
                                  verbose_name='Имя',
                                  blank=True)
    last_name = models.CharField(max_length=150,
                                 verbose_name='Фамилия',
                                 blank=True)
    bio = models.TextField(verbose_name='О себе',
                           blank=True,
                           null=True,
                           default='')
    role = models.CharField(max_length=9,
                            choices=USER_ROLES,
                            default=USER,
                            verbose_name='Роль')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'
        ordering = ['role', 'username']


class ConfirmationCode(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='confirmation_code')
    confirmation_code = models.CharField(max_length=6)
