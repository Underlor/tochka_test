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

    def json_serialise(self):
        return {
            'id': self.id,
            'name': self.name,
            'date': self.date.strftime('%m/%d/%Y'),
            'open': self.open,
            'higt': self.higt,
            'low': self.low,
            'close': self.close,
            'volume': self.volume,
        }

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

    def json_serialise(self):
        return {
            'id': self.id,
            'share': self.share,
            'name': self.name,
            'relation': self.relation,
            'lastdate': self.lastdate.strftime('%m/%d/%Y'),
            'transaction_type': self.transaction_type,
            'owner_type': self.owner_type,
            'shares_traded': self.shares_traded,
            'last_price': self.last_price,
            'shares_held': self.shares_held,
        }

    class Meta:
        db_table = 'parse_app_trader'
