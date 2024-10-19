from django.db import models
from solitonRE.models import 物件

# Create your models here.BK
class Broker(models.Model):
    BKID = models.CharField(max_length=30, primary_key=True)
    BK名 = models.CharField(max_length=100)
    BK担当者名 = models.CharField(max_length=20)
    BKEメール = models.CharField(max_length=50)
    BK電話番号 = models.CharField(max_length=20, blank=True, null=True)  
    BK会社番号 = models.CharField(max_length=20, blank=True, null=True)  
    BK住所 = models.CharField(max_length=100, blank=True, null=True)  
    BK短名 = models.CharField(max_length=20, blank=True, null=True)  

    def __str__(self):
        return self.BK短名

class UpdateReport(models.Model):
    BKID = models.ForeignKey(Broker, on_delete=models.CASCADE)
    RP日付 = models.DateField()
    RP内容 = models.CharField(max_length=255)
    物件ID = models.ForeignKey(物件, on_delete=models.DO_NOTHING)

