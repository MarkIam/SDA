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

class Certificate(models.Model):
    CERTIFICATE_STATUS = [
        ('IS', 'Issued'), # выпущен
        ('BO', 'Bought'), # приборетен
        ('US', 'Used'),   # использован
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
    skydiver = models.ForeignKey(Skydiver, on_delete=models.RESTRICT)
    
    OPERATION_TYPE = [
        ('WD', 'Wuthdraw'), # списание
        ('RF', 'Refill') # зачисление
    ]
    operation_type = models.CharField(max_length=2, choices=OPERATION_TYPE, verbose_name='Тип операции')

    amount = models.DecimalField(max_digits=6, decimal_places=0, verbose_name='Сумма операции в рублях')
    stamp = models.DateTimeField(auto_now=False, auto_now_add=False, verbose_name='Дата/время операции')

    def __str__(self):
        return self.skydiver.last_name + ', ' + self.operation_type + ' ' + self.amount

    class Meta:
        verbose_name = 'Операция по балансу'
        verbose_name_plural = 'Операции по балансу'

class CertificateBalanceOperation(models.Model):
    certificate = models.ForeignKey(Certificate, on_delete=models.RESTRICT)
    operation = models.ForeignKey(BalanceOperation, on_delete=models.RESTRICT)

    class Meta:
        verbose_name = 'Операция c сертификатом'
        verbose_name_plural = 'Операции c сертификатом'

class WithdrawalBalanceOperation(models.Model):
    operation = models.ForeignKey(BalanceOperation, on_delete=models.RESTRICT)
    services = models.ManyToManyField(SkydivingService)

    class Meta:
        verbose_name = 'Операция cписания за услуги'
        verbose_name_plural = 'Операции cписания за услуги'