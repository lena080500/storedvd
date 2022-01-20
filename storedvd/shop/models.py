from datetime import datetime

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
class Section(models.Model):
    #Название полей в таблице базы данных
    title = models.CharField(
        max_length = 70, #длина строки
        help_text = 'Надо ввести название раздела', #шаблон - подсказка
        unique = True, #уникальность
        verbose_name = 'Название раздела' #перевод
    )

    class Meta: #настройки способа отображения
        ordering = ['id'] #сортировка
        verbose_name = 'Раздел' #название в админке Section
        verbose_name_plural = 'Разделы'  # название в админке Section во множественном числе

    def __str__(self): #вариант отображения по умолчанию
        return self.title

class Product(models.Model): #таблица товаров
    sections = models.ForeignKey(
        'Section',  #соединение многие к одному с Section
        on_delete = models.SET_NULL, #если мы удалаем раздел, то остается пустое значение
        null = True, #раздел может быть не указан
        verbose_name = 'Раздел' #перевод
    )
    title = models.CharField(       #название товара
        max_length = 70,
        verbose_name = 'Название')
    image = models.ImageField(
        upload_to = 'images', #куда будет это все загружать (папка)
        verbose_name = 'Изображение'  #перевод
    )
    price = models.DecimalField(
        max_length = 10, #кол-во знаков
        decimal_places = 2, #кол-во после запятой
        verbose_name = 'Цена' #перевод
    )
    year = models.IntegerField(
        validators = [MinValueValidator(1900), #минимальный год
                      MaxValueValidator(datetime.date.today().year)], #максимальный год
        verbose_name = 'Год'
    )
    country = models.CharField(  #страна производитель
        max_length = 70,
        verbose_name ='Страна'
    )
    director = models.CharField(  #режисер
        max_length = 70,
        verbose_name ='Режисер'
    )
    play = models.IntegerField(   #продолжительность фильма
        validators=[MinValueValidator(1)],  # минимальная продолжительность
        null = True, #поле может быть пустым
        blank = True, #пользователь не будет обязан заполнять данное поле
        verbose_name = 'Продолжительность фильма',
        help_text = 'Укажите продолжительность в секундах'
    )
    cast = models.TextField(verbose_name = 'В ролях')
    description = models.TextField(verbose_name='Описание')
    date = models.DateField( #дата добавления товара или редактирования
        auto_now_add = True, #дата меняется при изменении параметров
        verbose_name='Дата добавленипя'
    )
    class Meta:  # настройки способа отображения
        ordering = ['title', 'year']  # сортировка по алфавиту, затем по году возрастанию
                                      #если '-year', то сортировка по убыванию
        verbose_name = 'Товар'  # название в админке Product
        verbose_name_plural = 'Товары'  # название в админке Product во множественном числе

    def __str__(self):
        return '{0} ({1})'.format(self.title, self.sections.title)

class Discount(models.Model): #скидки
    code = models.CharField(
        max_length = 10,
        verbose_name = 'Код купона'
    )
    value = models.IntegerField(    #значение размера скидки
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        verbose_name='Размер скидки',
        help_text = 'В процентах'
    )
    class Meta:  # настройки способа отображения
        ordering = ['-value']  # сортировка по размеру скидки
        verbose_name = 'Скидка'  # название в админке Product
        verbose_name_plural = 'Скидки'  # название в админке Product во множественном числе

    def __str__(self):
        return self.code + ' (' + str(self.value) + '%)'

class Order(models.Model):   #Заказы
    need_delivery = models.BooleanField(verbose_name='необходимость доставки'),
    discount = models.ForeignKey(Discount,
                                 verbose_name = 'Скидка',
                                 on_delete = models.SET_NULL(),
                                 null = True)
    name = models.CharField(max_length = 0,
                            verbose_name = 'Имя')
    phone = models.CharField(max_length = 70, verbose_name = 'Номер')
    email = models.EmailField()  #Email
    address = models.TextField(verbose_name = 'Адрес', blank = True) #может не заполнять, если не требуется доставка
    notice = models.TextField(blank = True, verbose_name = 'Примечание к заказу') #комментарий
    date_order = models.DateTimeField(
        auto_now_add = True,  #берется текущая дата со временем
        verbose_name = 'Дата заказа',
    )
    date_send = models.DateTimeField(
        null = True,
        blank= True,
        verbose_name = 'Дата отправки',
    )
    STATUSES = [  #Статус заказа
        ('New', 'Новый заказ'),  #значение статуса и его перевод
        ('Apr', 'Подтвержден'),
        ('Pay', 'Опдачен'),
        ('Cnl', 'Отменен')
    ]
    status = models.CharField(choices = STATUSES, max_length = 3, default = 'New', verbose_name = 'Статус')
    class Meta:  # настройки способа отображения
        ordering = ['date']  # сортировка по размеру скидки
        verbose_name = 'Заказ'  # название в админке Order
        verbose_name_plural = 'Заказы'  # название в админке Order во множественном числе

    def __str__(self):
        return 'ID:' + str(self.id)
