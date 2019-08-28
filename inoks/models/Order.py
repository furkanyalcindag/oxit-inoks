from django.db import models

from inoks.models import Profile, City, District

from inoks.models.OrderSituations import OrderSituations
from inoks.models.Product import Product


class Order(models.Model):
    DOOR = 'Kapıda Ödeme'
    CREDIT = 'Kredi Kartı'
    TRANSFER = 'Havale/EFT'
    PAYMENT_CHOICES = (
        (DOOR, 'Kapıda Ödeme'),
        (CREDIT, 'Kredi Kartı'),
        (TRANSFER, 'Havale/EFT'),
    )

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Üye Adı')
    product = models.ManyToManyField(Product)
    order_situations = models.ManyToManyField(OrderSituations, default='Ödeme Bekliyor')
    quantity = models.IntegerField(null=True, blank=True, verbose_name='Sipariş Adeti')
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name='İl')
    district = models.ForeignKey(District, on_delete=models.CASCADE, verbose_name='İlçe', default=None)
    address = models.TextField(blank=True, null=True, verbose_name='Adres')
    sponsor = models.TextField(blank=True, null=True, verbose_name='Sponsor')
    payment_type = models.CharField(max_length=128, verbose_name='Ödeme Türü', choices=PAYMENT_CHOICES, default=DOOR)
    isContract = models.BooleanField(default=False)
    isApprove = models.BooleanField(default=False)
    isPayed = models.BooleanField(default=False)
    creationDate = models.DateTimeField(auto_now_add=True, verbose_name='Kayıt Tarihi')
    modificationDate = models.DateTimeField(auto_now=True, verbose_name='Güncelleme Tarihi')

    def __str__(self):
        return '%d ' % self.id