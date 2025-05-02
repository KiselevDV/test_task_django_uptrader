import logging

from django.db import models
from django.urls import reverse, NoReverseMatch


logger = logging.getLogger(__name__)


class Menu(models.Model):
    """Модель меню"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название меню')

    class Meta:
        verbose_name = 'Меню'
        verbose_name_plural = 'Меню'

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    """Пункт меню. Поддерживает иерархию через parent"""
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    url = models.CharField(max_length=255, blank=True, verbose_name='Явный URL')
    named_url = models.CharField(max_length=100, blank=True, verbose_name='Именованный URL')
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name='items', verbose_name='Меню', db_index=True)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='children',
        null=True, blank=True, verbose_name='Родительский пункт', db_index=True
    )

    class Meta:
        verbose_name = 'Пункт меню'
        verbose_name_plural = 'Пункты меню'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Абсолютный URL по named_url / url"""
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                logger.warning(f'Именованный URL \"{self.named_url}\" '
                               f'не найден для пункта \"{self.title}\" (ID={self.id})')
        return self.url if self.url else '/'
