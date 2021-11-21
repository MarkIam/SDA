from django.db import models

class Skydiver(models.Model):
    first_name = models.CharField(max_length=64, verbose_name='Имя')
    last_name = models.CharField(max_length=64, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=64, verbose_name='Отчество')
    birth_date = models.DateField(verbose_name='Дата рождения')
    passport_number = models.CharField(max_length=10, verbose_name='Серия и номер паспорта')
    passport_data = models.TextField(max_length=256, verbose_name='Кем и когда выдан паспорт')
    email = models.EmailField(verbose_name='Электронная почта', blank=True)
    phone_number = models.CharField(max_length=10, verbose_name='Номер телефона')

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        unique_together = ('last_name', 'first_name', 'patronymic', 'passport_number')
        # ordering = ['last_name']
        # abstract = True