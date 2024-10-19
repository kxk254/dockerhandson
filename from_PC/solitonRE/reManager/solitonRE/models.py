from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

###　テナント設定を設定する
class テナント(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  #
    テナント名 = models.CharField(max_length=255) 
    テナント短縮名 = models.CharField(max_length=255, blank=True) 
    テナント住所 = models.CharField(max_length=255) 
    テナント電話番号 = models.CharField(max_length=15)  
    テナント担当者名 = models.CharField(max_length=255) 
    テナントソート = models.CharField(max_length=10, blank=True, null=True)  

    def __str__(self):
        return self.テナント短縮名  # Return tenant name as string representation

###　物件設定を設定する
class 物件(models.Model):
    id = models.AutoField(primary_key=True)
    物件名 = models.CharField(max_length=100)
    物件住所 = models.CharField(max_length=200)
    物件種類 = models.CharField(max_length=100)
    建築年月日 = models.DateField()
    敷地面積 = models.FloatField()  
    床面積 = models.FloatField()  
    構造  = models.CharField(max_length=100)

    def __str__(self):
        return self.物件名  # Return tenant name as string representation

###　管理項目設定を設定する
class 管理項目(models.Model):
    管理項目コード = models.CharField(max_length=32, primary_key=True)
    管理項目印字名 = models.CharField(max_length=100)
    管理項目短縮名 = models.CharField(max_length=50, blank=True) 
    管理項目レポート分類区分 = models.CharField(max_length=100)

    def __str__(self):
        return self.管理項目短縮名  # Return tenant name as string representation

###　保証会社設定を設定する
class 保証会社(models.Model):
    保証会社コード = models.CharField(max_length=32, primary_key=True)
    保証会社名 = models.CharField(max_length=100)
    保証会社住所 = models.CharField(max_length=200)
    保証会社担当者名 = models.CharField(max_length=100)
    保証会社連絡先 = models.CharField(max_length=100)

    def __str__(self):
        return self.保証会社名 

###　契約項目を設定する
class 契約(models.Model):
    契約ID = models.CharField(max_length=32, primary_key=True)
    テナントID = models.ForeignKey(テナント, on_delete=models.CASCADE)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    部屋番号 = models.CharField(max_length=24)
    契約日 = models.DateField()
    当初開始日 = models.DateField()
    当初終了日 = models.DateField()
    現在契約開始日 = models.DateField(blank=True, null=True)
    現在契約終了日 = models.DateField(blank=True, null=True)
    賃料金額 = models.IntegerField()
    共益費 = models.IntegerField()
    契約種類 = models.CharField(max_length=100)
    自動更新 = models.BooleanField(default=True)
    契約年数 = models.CharField(max_length=20)
    更新料有無 = models.BooleanField(default=True)
    更新料金額 = models.IntegerField()
    解約通知期間 = models.CharField(max_length=20)
    居室タイプ = models.CharField(max_length=32)
    平米数 = models.FloatField()   # Square footage of the room
    坪数 = models.FloatField()    # per tsubo 
    保証金金額 = models.IntegerField()
    保証金月数 = models.IntegerField()
    保証有無 = models.BooleanField(default=True, null=True)
    保証会社コード = models.ForeignKey(保証会社, on_delete=models.CASCADE)
    フリーレント = models.CharField(max_length=200, blank=True, null=True)
    備考 = models.CharField(max_length=200, blank=True, null=True)
    delete_flag = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.物件ID}-{self.部屋番号}"  # Return tenant name as string representation

###　支払先設定を設定する
class 支払先(models.Model):
    支払先コード = models.CharField(max_length=32, primary_key=True)
    請求先名 = models.CharField(max_length=100)
    請求先住所 = models.CharField(max_length=200)
    請求先担当者 = models.CharField(max_length=100)
    請求先電話番号 = models.CharField(max_length=100) 

    def __str__(self):
        return self.請求先名

###　敷金保証金を設定する
class 敷金保証金(models.Model):
    id = models.AutoField(primary_key=True)
    契約番号 = models.ForeignKey(契約, on_delete=models.CASCADE)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    テナントID = models.ForeignKey(テナント, on_delete=models.CASCADE)
    契約区画 = models.CharField(max_length=100)
    定借区分 = models.CharField(max_length=100)
    種類 = models.CharField(max_length=100)
    前月末残高 = models.IntegerField(blank=True, null=True)
    当月増額 = models.IntegerField(blank=True, null=True)
    当月減少 = models.IntegerField(blank=True, null=True)
    今月末残高 = models.IntegerField()
    移動予定日 = models.CharField(max_length=255, blank=True, null=True)
    保証会社コード = models.ForeignKey(保証会社, on_delete=models.CASCADE)
    備考 = models.CharField(max_length=255, blank=True, null=True)
    DeleteFlag = models.BooleanField(default=False)

class 売上(models.Model):
    id = models.AutoField(primary_key=True)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    テナントID = models.ForeignKey(テナント, on_delete=models.CASCADE)
    管理項目コード = models.ForeignKey(管理項目, on_delete=models.CASCADE)
    契約ID = models.ForeignKey(契約, on_delete=models.CASCADE)
    レポート日 = models.DateField()
    該当月開始月 = models.DateField()
    該当月終了月 = models.DateField()
    請求書発行日 = models.DateField()
    入金予定日 = models.DateField(blank=True, null=True)
    計上日 = models.DateField(blank=True, null=True)
    請求金額 = models.IntegerField(blank=True, null=True)
    請求消費税 = models.IntegerField(blank=True, null=True)
    請求税込金額 = models.IntegerField(blank=True, null=True)
    当月入金日 = models.DateField(blank=True, null=True)
    備考 = models.CharField(max_length=200, blank=True, null=True)
    DeleteFlag = models.BooleanField(default=False)

#費用入力を設定する 費用InputView
class 費用(models.Model):
    id = models.AutoField(primary_key=True)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    支払先コード = models.ForeignKey(支払先, on_delete=models.CASCADE)
    管理項目コード = models.ForeignKey(管理項目, on_delete=models.CASCADE)
    レポート日 = models.DateField()
    当該月開始月 = models.DateField()
    当該月終了月 = models.DateField()
    請求書発行月 = models.DateField()
    計上日 = models.DateField(blank=True, null=True)
    請求金額 = models.IntegerField(blank=True, null=True)
    請求消費税 = models.IntegerField(blank=True, null=True)
    請求税金込 = models.IntegerField(blank=True, null=True)
    当月支払日 = models.DateField(blank=True, null=True)
    備考 = models.CharField(max_length=255, null=True, blank=True)
    DeleteFlag = models.BooleanField(default=False)

###　ステータスを設定する
class ステータス(models.Model):
    id = models.AutoField(primary_key=True)
    レポート日 = models.DateField()
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    新テナント = models.CharField(max_length=255, null=True, blank=True)
    テナント関連 = models.CharField(max_length=255, null=True, blank=True)
    遅延状況 = models.CharField(max_length=255, null=True, blank=True)
    検査情報 = models.CharField(max_length=255, null=True, blank=True)
    メンテナンス = models.CharField(max_length=255, null=True, blank=True)
    その他 = models.CharField(max_length=255, null=True, blank=True)
    特別項目 = models.CharField(max_length=255, null=True, blank=True)
    DeleteFlag = models.BooleanField(default=False)

class MonthSelect(models.Model):
    MonthSelect = models.DateField(primary_key=True)

#入力項目を設定
class InputField(models.Model):
    id = models.AutoField(primary_key=True)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    テナントID = models.ForeignKey(テナント, on_delete=models.CASCADE)
    契約ID = models.ForeignKey(契約, on_delete=models.CASCADE, null=True, blank=True)
    管理項目コード = models.ForeignKey(管理項目, on_delete=models.CASCADE)
    請求金額 = models.IntegerField(blank=True, null=True)

#BM作業内容の説明 BM_item_input.html
###　BM項目設定を設定する（ソートはなし。ただ項目を設定するのみ。）
class BMItems(models.Model):
    id = models.AutoField(primary_key=True)
    BM項目 = models.CharField(max_length=30)
    BM項目CD = models.CharField(max_length=30)
    BM内容説明 = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.BM項目

#物件ごとのBM作業、予定日程を決定 BMinput_field.html
###　BM入力を設定する（物件ソート）
class BMInputField(models.Model):
    id = models.AutoField(primary_key=True)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    BM項目 = models.ForeignKey(BMItems, on_delete=models.CASCADE)
    BM回数 = models.CharField(max_length=30)
    BM予定数 = models.CharField(max_length=30)

#物件の月次報告フォーム　BM_input_view.html
###　BM報告を設定する（物件及び年月でソート）
class BM入力フォーム(models.Model):
    id = models.AutoField(primary_key=True)
    物件ID = models.ForeignKey(物件, on_delete=models.CASCADE)
    レポート日 = models.DateField()
    BM項目 = models.ForeignKey(BMItems, on_delete=models.CASCADE)
    BM回数 = models.CharField(max_length=30)
    BM予定数 = models.CharField(max_length=30)
    BM予定 = models.CharField(max_length=30, null=True, blank=True)
    BM実施 = models.CharField(max_length=30, null=True, blank=True)
    BMコメント = models.CharField(max_length=255, null=True, blank=True)






