from django.db import models


# Create your models here.

class data_1688(models.Model):
    item = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    supplier = models.CharField(max_length=50, blank=True)
    sale = models.DecimalField(decimal_places=0, max_digits=10, blank=True)
    link = models.CharField(max_length=500, blank=True)


class data_taobao(models.Model):
    item = models.CharField(max_length=100, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    supplier = models.CharField(max_length=50, blank=True)
    location = models.CharField(max_length=20, blank=True)
    sale = models.DecimalField(decimal_places=0, max_digits=10, blank=True)
    link = models.CharField(max_length=500, blank=True)


class data_jd(models.Model):
    item = models.CharField(max_length=100, blank=True)
    price = models.CharField(max_length=100, blank=True)
    supplier = models.CharField(max_length=50, blank=True)
    rate = models.DecimalField(decimal_places=0, max_digits=10, blank=True)
    link = models.CharField(max_length=500, blank=True)
    comment_id = models.CharField(max_length=100, blank=True)


class essencial_field(models.Model):
    jd_header = models.TextField(max_length=1000, blank=True, default='')
    jd_comment_header = models.TextField(max_length=1000, blank=True, default='')
    jd_comment_cookie = models.TextField(max_length=1000, blank=True, default='')
    tb_header = models.TextField(max_length=1000, blank=True, default='')
    pjjx_header = models.TextField(max_length=1000, blank=True, default='')


class users(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=100)