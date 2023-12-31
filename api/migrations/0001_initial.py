# Generated by Django 4.1.6 on 2023-12-24 09:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='InstrumentalService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200, verbose_name='Номи')),
                ('service_price', models.FloatField(default=0, verbose_name='Нархи')),
            ],
            options={
                'verbose_name': 'Инструментал хизмат номи',
                'verbose_name_plural': 'Инструментал хизматлар',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='MainService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=200, verbose_name='Номи')),
            ],
            options={
                'verbose_name': 'Курик гурух',
                'verbose_name_plural': 'Курик гурухлари',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug_name', models.CharField(blank=True, max_length=200, null=True)),
                ('full_name', models.CharField(max_length=200, verbose_name='Ф.И.О')),
                ('pass_data', models.CharField(max_length=50, verbose_name='Паспорт сериа')),
                ('phone_number', models.CharField(max_length=50, verbose_name='Тел. ракам')),
                ('address', models.CharField(max_length=255, verbose_name='Манзил')),
                ('workplace', models.CharField(max_length=200, verbose_name='Иш жойи')),
                ('inspaction', models.CharField(max_length=100, verbose_name='Режим тури')),
                ('birthday', models.DateField(null=True, verbose_name='Тугилган сана')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Руйхатдан утган сана')),
                ('duration', models.IntegerField(blank=True, null=True, verbose_name='Муддати')),
                ('analysis_status', models.BooleanField(default=False, verbose_name='Тахлил')),
                ('doctor_status', models.BooleanField(default=False, verbose_name='Доктор куриги')),
                ('conclusion', models.TextField(blank=True, null=True, verbose_name='Хулоса')),
                ('room_status', models.BooleanField(default=False, verbose_name='Хонадан чикариш')),
                ('discount', models.FloatField(default=0, verbose_name='Чегирма')),
            ],
            options={
                'verbose_name': 'Бемор',
                'verbose_name_plural': 'Беморлар',
            },
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_number', models.CharField(max_length=150, verbose_name='Раками')),
                ('room_personal', models.IntegerField(verbose_name='Сигим')),
                ('room_price', models.FloatField(verbose_name='Нархи')),
            ],
            options={
                'verbose_name': 'Хона',
                'verbose_name_plural': 'Хоналар',
                'ordering': ('room_number',),
            },
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=200, verbose_name='Ф.И.О')),
                ('position', models.CharField(choices=[('labarant', 'labarant'), ('reception', 'reception'), ('doctor', 'doctor')], max_length=200, verbose_name='Лавозим')),
                ('price', models.FloatField(blank=True, default=0, null=True, verbose_name='Иш хаки')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Аккаунт')),
            ],
            options={
                'verbose_name': 'Ходим',
                'verbose_name_plural': 'Ходимлар',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=255, verbose_name='Номи')),
                ('service_unit', models.CharField(blank=True, max_length=255, null=True, verbose_name='Улчов бирлиги')),
                ('service_norm', models.CharField(blank=True, max_length=255, null=True, verbose_name='Норма')),
                ('service_price', models.FloatField(default=0, verbose_name='Нархи')),
                ('rec_visible', models.BooleanField(default=True, verbose_name='Руйхатга олишда курсатиш')),
                ('tab_visible', models.BooleanField(default=True, verbose_name='Беморнинг тахлил натижаларида курсатиш курсатиш')),
                ('service_id', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.mainservice', verbose_name='Хизмат тури')),
            ],
            options={
                'verbose_name': 'Курик тури',
                'verbose_name_plural': 'Курик турлари',
            },
        ),
        migrations.CreateModel(
            name='PatientService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_checked', models.BooleanField(default=True, verbose_name='Танланган')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.service')),
            ],
            options={
                'verbose_name': 'Бемор куриги',
                'verbose_name_plural': 'Беморлар куриклари',
            },
        ),
        migrations.AddField(
            model_name='patient',
            name='doctor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='doctor', to='api.staff', verbose_name='Доктор'),
        ),
        migrations.AddField(
            model_name='patient',
            name='instrumental_service',
            field=models.ManyToManyField(blank=True, null=True, to='api.instrumentalservice', verbose_name='Инструментал курик турлари'),
        ),
        migrations.AddField(
            model_name='patient',
            name='room',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.room', verbose_name='Хона раками'),
        ),
        migrations.AddField(
            model_name='patient',
            name='staff',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff', to='api.staff', verbose_name='Руйхатга олувчи'),
        ),
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, max_length=50, null=True, verbose_name='Натижа')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Текширилган сана')),
                ('is_checked', models.BooleanField(default=True, verbose_name='Танланган')),
                ('patient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.patient', verbose_name='Бемор')),
                ('service', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.patientservice', verbose_name='Курик турлари')),
            ],
            options={
                'verbose_name': 'Тахлил',
                'verbose_name_plural': 'Тахлиллар',
            },
        ),
    ]
