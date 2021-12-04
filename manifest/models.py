from django.contrib import admin
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
    weight = models.FloatField(verbose_name='Вес', blank=True, default=75)

    def __str__(self):
        return self.last_name + ' ' + self.first_name

    def get_absolute_url(self):
        pass

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
        unique_together = ('last_name', 'first_name', 'patronymic', 'passport_number')

class GiftCertificate(models.Model):
    CERTIFICATE_STATUS = [
        ('IS', 'Выпущен'),
        ('BO', 'Приобретен'),
        ('US', 'Использован')
    ]
    status = models.CharField(max_length=2, choices=CERTIFICATE_STATUS, verbose_name='Текущий статус сертификата')
    number = models.CharField(max_length=10, verbose_name='Номер сертификата')
    nominal = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Номинал сертификата в рублях')
    issued_stamp = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name='Дата/время выпуска сертификата')
    acquisition_stamp = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата/время приобретения сертификата')
    usage_stamp = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата/время использования сертификата')

    def __str__(self):
        return self.number

    class Meta:
        verbose_name = 'Сертификат'
        verbose_name_plural = 'Сертификаты'

class SkydivingService(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название услуги')
    price = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Стоимость услуги в рублях')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'

class BalanceOperation(models.Model):
    skydiver = models.ForeignKey(Skydiver, on_delete=models.RESTRICT, verbose_name='Клиент')
    
    OPERATION_TYPE = [
        ('WD', 'Cписание'),
        ('RF', 'Зачисление')
    ]
    operation_type = models.CharField(max_length=2, choices=OPERATION_TYPE, verbose_name='Тип операции')

    amount = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Сумма операции в рублях')
    stamp = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата/время операции')

    def __str__(self):
        return self.skydiver.last_name + ', ' + self.operation_type + ' ' + str(self.amount)

    class Meta:
        verbose_name = 'Операция по балансу'
        verbose_name_plural = 'Операции по балансу'

class CertificateBalanceOperation(models.Model):
    certificate = models.ForeignKey(to=GiftCertificate, on_delete=models.RESTRICT, verbose_name='Сертификат')
    operation = models.ForeignKey(to=BalanceOperation, on_delete=models.RESTRICT, verbose_name='Операция')

    def __str__(self):
        return self.certificate.number + ', ' + str(self.operation.amount)

    class Meta:
        verbose_name = 'Операция c сертификатом'
        verbose_name_plural = 'Операции c сертификатом'

class WithdrawalBalanceOperation(models.Model):
    operation = models.ForeignKey(BalanceOperation, on_delete=models.RESTRICT)
    services = models.ManyToManyField(SkydivingService)

    class Meta:
        verbose_name = 'Операция cписания за услуги'
        verbose_name_plural = 'Операции cписания за услуги'

class SkydiveDiscipline(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название дисциплины')
    short_name = models.CharField(max_length=10, verbose_name='Короткое название дисциплины', default='-')
    description = models.TextField(max_length=1000, verbose_name='Описание дисциплины', default='-')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дисциплина'
        verbose_name_plural = 'Дисциплины'

class SkydiverRequest(models.Model):
    skydiver = models.ForeignKey(to=Skydiver, on_delete=models.RESTRICT, verbose_name='Клиент')
    creationStamp = models.DateTimeField(verbose_name='Дата/время создания заявки')
    discipline = models.ForeignKey(to=SkydiveDiscipline, on_delete=models.RESTRICT, verbose_name='Дисциплина', default=1)
    height = models.FloatField(verbose_name='Высота прыжка', default=1200)

    REQUEST_STATUS = [
        ('CR', 'Создана'),
        ('MNF', 'Включена в подъем'),
        ('CMP', 'Выполнена')
    ]
    status = models.CharField(max_length=3, choices=REQUEST_STATUS, verbose_name='Текущий статус заявки')

    def __str__(self):
        return self.skydiver.last_name + ' ' + self.skydiver.first_name + ', ' + self.discipline.name + ', ' + str(self.height)

    class Meta:
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'

class RequestService(models.Model):
    request = models.ForeignKey(SkydiverRequest,on_delete=models.CASCADE,null=True, verbose_name='Заявка')
    service = models.ForeignKey(SkydivingService,on_delete=models.PROTECT,null=True, verbose_name='Услуга')
    quantity = models.FloatField(verbose_name='Количество')

    class Meta:
        verbose_name = 'Услуга в заявке'
        verbose_name_plural = 'Услуги в заявке'


class PlaneType(models.Model):
    name = models.CharField(max_length=64, verbose_name='Название типа воздушного судна')
    default_capacity = models.SmallIntegerField(verbose_name='Вместительность по умолчанию')
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Тип воздушного судна'
        verbose_name_plural = 'Типы воздушных суден'

class Plane(models.Model):
    plane_type = models.ForeignKey(to=PlaneType, on_delete=models.RESTRICT, verbose_name='Тип воздушного судна')
    reg_number = models.CharField(max_length=10, verbose_name='Регистрационный номер воздушного судна')
    capacity = models.SmallIntegerField(verbose_name='Вместительность')

    def __str__(self):
        return self.plane_type.name + ',' + self.reg_number

    class Meta:
        verbose_name = 'Воздушное судно'
        verbose_name_plural = 'Воздушные судна'

class PlaneLift(models.Model):
    plane = models.ForeignKey(to = Plane, on_delete=models.RESTRICT, verbose_name='Воздушное судно')
    day = models.DateField(verbose_name='Дата подъема')
    ord_number = models.SmallIntegerField(verbose_name='Порядковый номер')

    LIFT_STATUS = [
        ('CR', 'Создан'), 
        ('PL', 'Запланирован'),
        ('FRM', 'Сформирован'),
        ('RD', 'Готов к взлету'),
        ('IP', 'В воздухе'),
        ('CMP', 'Завершен'),
        ('CNC', 'Отменен')
    ]
    status = models.CharField(max_length=3, choices=LIFT_STATUS, verbose_name='Текущий статус подъема')
    request = models.ManyToManyField(to=SkydiverRequest, verbose_name='Заявки в подъеме')

    def __str__(self):
        return str(self.ord_number) + ',' + self.plane.reg_number + ',' + self.day.strftime('%d.%m.%Y')

    class Meta:
        verbose_name = 'Подъем воздушного судна'
        verbose_name_plural = 'Подъемы воздушных суден'