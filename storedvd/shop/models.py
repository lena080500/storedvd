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