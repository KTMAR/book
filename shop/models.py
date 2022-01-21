from django.conf import settings
from django.db import models

from utils import upload_function
from django.db import models


class Writer(models.Model):
    """Писатель"""

    name = models.CharField(max_length=255, verbose_name='Писатель')
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    slug = models.SlugField()
    image = models.ImageField(upload_to=upload_function, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Писатель'
        verbose_name_plural = 'Писатели'


class MediaType(models.Model):
    """Формат носителя"""

    name = models.CharField(max_length=100, verbose_name='Тип носителя')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип носителя'
        verbose_name_plural = 'Тип носителей'


class Genre(models.Model):
    """Жанр книги"""

    name = models.CharField(max_length=50, verbose_name='Название жанра')
    slug = models.SlugField()

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Book(models.Model):
    """Книга"""

    writer = models.ForeignKey(Writer, on_delete=models.CASCADE, verbose_name='Писатель')
    name = models.CharField(max_length=255, verbose_name='Название книги')
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    media_type = models.ForeignKey(MediaType, verbose_name='Носитель', on_delete=models.CASCADE)
    release_date = models.DateField(verbose_name='Дата релиза')
    slug = models.SlugField()
    description = models.TextField(verbose_name='Описание', default='Описание отсутствует')
    stock = models.IntegerField(default=1, verbose_name='Наличие')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Предолжение недели?')
    image = models.ImageField(upload_to=upload_function)

    def __str__(self):
        return f'{self.id} | {self.writer.name} | {self.name}'

    def ct_model(self):
        return self._meta.model_name

    class Meta:
        verbose_name = "Книга"
        verbose_name_plural = 'Книги'


class Customer(models.Model):
    """Покупатель"""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, verbose_name='Пользователь', on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True, verbose_name='Активный?')
    # customer_orders = models.ManyToManyField(Order, blank=True, verbose_name='Заказы', related_name='related_customer')
    wishlist = models.ManyToManyField(Book, blank=True, verbose_name='Список ожидаемого')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.TextField(max_length=100, null=True, blank=True, verbose_name='Адрес')

    def __str__(self):
        return f'{self.user.username}'

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'
