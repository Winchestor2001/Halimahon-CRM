from django.db import models
from django.contrib.auth.models import User


class Staff(models.Model):
    POSITION = (
        ('labarant', 'labarant'),
        ('reception', 'reception'),
        ('doctor', 'doctor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Аккаунт")
    full_name = models.CharField(max_length=200, verbose_name="Ф.И.О")
    position = models.CharField(max_length=200, choices=POSITION, verbose_name="Лавозим")
    price = models.FloatField(default=0, blank=True, null=True, verbose_name="Иш хаки")

    def __str__(self) -> str:
        return f"{self.full_name} - {self.position}"

    class Meta:
        verbose_name = "Ходим"
        verbose_name_plural = "Ходимлар"


class MainService(models.Model):
    service_name = models.CharField(max_length=200, verbose_name="Номи")

    def __str__(self) -> str:
        return f"{self.service_name}"

    class Meta:
        verbose_name = "Курик гурух"
        verbose_name_plural = "Курик гурухлари"
        ordering = ('id',)


class InstrumentalService(models.Model):
    service_name = models.CharField(max_length=200, verbose_name="Номи")
    service_price = models.FloatField(default=0, verbose_name="Нархи")

    def __str__(self) -> str:
        return f"{self.service_name}"

    class Meta:
        verbose_name = "Инструментал хизмат номи"
        verbose_name_plural = "Инструментал хизматлар"
        ordering = ('id',)


class Service(models.Model):
    service_id = models.ForeignKey(MainService, on_delete=models.CASCADE, null=True, blank=True,
                                   verbose_name="Хизмат тури")
    service_name = models.CharField(max_length=255, verbose_name="Номи")
    service_unit = models.CharField(max_length=255, blank=True, null=True, verbose_name="Улчов бирлиги")
    service_norm = models.CharField(max_length=255, blank=True, null=True, verbose_name="Норма")
    service_price = models.FloatField(default=0, verbose_name="Нархи")
    rec_visible = models.BooleanField(default=True, verbose_name="Руйхатга олишда курсатиш")
    tab_visible = models.BooleanField(default=True, verbose_name="Беморнинг тахлил натижаларида курсатиш курсатиш")

    def __str__(self) -> str:
        return str(self.service_name)

    class Meta:
        verbose_name = "Курик тури"
        verbose_name_plural = "Курик турлари"


class Room(models.Model):
    room_number = models.CharField(max_length=150, verbose_name="Раками")
    room_personal = models.IntegerField(verbose_name="Сигим")
    room_price = models.FloatField(verbose_name="Нархи")

    def __str__(self) -> str:
        return str(self.room_number)

    class Meta:
        ordering = ('room_number',)
        verbose_name = "Хона"
        verbose_name_plural = "Хоналар"


class Patient(models.Model):
    slug_name = models.CharField(max_length=200, null=True, blank=True)
    doctor = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='doctor', null=True, blank=True,
                               verbose_name="Доктор")
    full_name = models.CharField(max_length=200, verbose_name="Ф.И.О")
    pass_data = models.CharField(max_length=50, verbose_name="Паспорт сериа")
    phone_number = models.CharField(max_length=50, verbose_name="Тел. ракам")
    address = models.CharField(max_length=255, verbose_name="Манзил")
    workplace = models.CharField(max_length=200, verbose_name="Иш жойи")
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE, related_name='staff', verbose_name="Руйхатга олувчи")
    inspaction = models.CharField(max_length=100, verbose_name="Режим тури")
    birthday = models.DateField(null=True, verbose_name="Тугилган сана")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Руйхатдан утган сана")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, blank=True, null=True, verbose_name="Хона раками")
    duration = models.IntegerField(blank=True, null=True, verbose_name="Муддати")
    instrumental_service = models.ManyToManyField(InstrumentalService, null=True, blank=True,
                                                  verbose_name="Инструментал курик турлари")
    analysis_status = models.BooleanField(default=False, verbose_name="Тахлил")
    doctor_status = models.BooleanField(default=False, verbose_name="Доктор куриги")
    conclusion = models.TextField(null=True, blank=True, verbose_name="Хулоса")
    room_status = models.BooleanField(default=False, verbose_name="Хонадан чикариш")
    discount = models.FloatField(default=0, verbose_name="Чегирма")

    def __str__(self) -> str:
        return str(self.full_name)

    class Meta:
        verbose_name = "Бемор"
        verbose_name_plural = "Беморлар"


class PatientService(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    is_checked = models.BooleanField(default=True, verbose_name="Танланган")

    def __str__(self) -> str:
        return f"{self.patient} - {self.service}"

    class Meta:
        verbose_name = "Бемор куриги"
        verbose_name_plural = "Беморлар куриклари"


class Analysis(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Бемор")
    result = models.CharField(max_length=50, blank=True, null=True, verbose_name="Натижа")

    service = models.ForeignKey(PatientService, on_delete=models.CASCADE, null=True, blank=True,
                                verbose_name="Курик турлари")

    created_date = models.DateTimeField(auto_now_add=True, verbose_name="Текширилган сана")

    is_checked = models.BooleanField(default=True, verbose_name="Танланган")

    def __str__(self) -> str:
        return str(self.patient)

    class Meta:
        verbose_name = "Тахлил"
        verbose_name_plural = "Тахлиллар"
