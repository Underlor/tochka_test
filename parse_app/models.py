from django.db import models


# Create your models here.
class Share(models.Model):
    name = models.CharField(max_length=32)
    date = models.DateField()
    open = models.FloatField(default=0)
    higt = models.FloatField(default=0)
    low = models.FloatField(default=0)
    close = models.FloatField(default=0)
    volume = models.IntegerField(default=0)

    class Meta:
        db_table = 'parse_app_share'


class Trader(models.Model):
    share = models.CharField(max_length=32)
    name = models.CharField(max_length=32)
    relation = models.CharField(max_length=32)
    lastdate = models.DateField()
    transaction_type = models.CharField(max_length=32)
    owner_type = models.CharField(max_length=32)
    shares_traded = models.IntegerField()
    last_price = models.FloatField()
    shares_held = models.IntegerField()

    class Meta:
        db_table = 'parse_app_trader'
