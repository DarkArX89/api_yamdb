# Generated by Django 3.2 on 2023-04-04 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_user_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('user', 'user'), ('admin', 'administrator'), ('moderator', 'moderator')], default='user', max_length=9, verbose_name='Роль'),
        ),
    ]