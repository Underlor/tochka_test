from django.db import models


# Create your models here.
class Share(models.Model):
    open = models.IntegerField(default=0)
    higt = models.IntegerField(default=0)
    low = models.IntegerField(default=0)
    close = models.IntegerField(default=0)
    volume = models.IntegerField(default=0)

    class Meta:
        db_table = 'parse_app_shere'
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'
