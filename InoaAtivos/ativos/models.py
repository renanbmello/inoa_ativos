from django.db import models


class Ativo (models.Model):
    id = models.AutoField(primary_key=True)
    longName = models.CharField(max_length=255, default='')
    symbol = models.CharField(max_length=255, default='')
    sector = models.CharField(max_length=255, default='')
    profitMargins = models.CharField(max_length=255, default='')
    stocks = models.JSONField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Symbol (models.Model):
    name = models.CharField(max_length=20)
