from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

STATUSES = [('for moderation', 'на модерацию'), ('published', 'опубликовано'), ('rejected', 'отклонено'),
            ('for deletion', 'на удаление')]


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название')


class Announcement(models.Model):
    picture = models.ImageField(verbose_name='Фотография', upload_to='photos', null=True, blank=True)
    title = models.CharField(max_length=50, verbose_name='Заголовок')
    description = models.TextField(max_length=500, null=True, blank=True, verbose_name='Описание')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='announcements_a',
                               verbose_name='Автор')
    category = models.ForeignKey('webapp.Category', on_delete=models.CASCADE, related_name='announcements_c',
                                 verbose_name='Категория')
    price = models.IntegerField(verbose_name='Цена', validators=(MinValueValidator(1),))
    status = models.CharField(max_length=30, default='for moderation', choices=STATUSES, verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания')
    published_at = models.DateTimeField(verbose_name='Дата-время публикации')
    edited_at = models.DateTimeField(auto_now=True, verbose_name='Дата-время редактирования')

    def __str__(self):
        return f"{self.title}"


class Comment(models.Model):
    text = models.TextField(max_length=500, verbose_name='Текст комментария')
    author = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='comments_a', verbose_name='Автор')
    announcement = models.ForeignKey('webapp.Announcement', on_delete=models.CASCADE, related_name='comments_anc',
                                verbose_name='Объявление')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата-время создания')

    def __str__(self):
        return f"{self.author.username}"
