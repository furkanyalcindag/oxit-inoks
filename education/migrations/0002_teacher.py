# Generated by Django 2.2.1 on 2019-05-31 12:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('education', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profileImage', models.ImageField(blank=True, null=True, upload_to='profile/', verbose_name='Profil Resmi')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Adres')),
                ('mobilePhone', models.CharField(max_length=120, verbose_name='Telefon Numarası')),
                ('gender', models.CharField(choices=[('Erkek', 'Erkek'), ('Kadın', 'Kadın')], default='Erkek', max_length=128, verbose_name='Cinsiyeti')),
                ('tc', models.CharField(blank=True, max_length=128, null=True, verbose_name='T.C. Kimlik Numarası')),
                ('birthDate', models.DateField(null=True, verbose_name='Doğum Tarihi')),
                ('creationDate', models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')),
                ('modificationDate', models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'permissions': (('teacher_add', 'Öğretmen Ekle'), ('teacher_list', 'Öğretmen Liste'), ('update_teacher', 'Öğretmen Güncelle')),
            },
        ),
    ]