from django.contrib import admin
from .models import User, テナント, 物件, 管理項目, 契約, 支払先, 保証会社, 敷金保証金, 売上, 費用, ステータス, MonthSelect, BMItems

# Register your models here.
@admin.register(User)
class User(admin.ModelAdmin):
    pass

@admin.register(テナント)
class テナント(admin.ModelAdmin):
    pass

@admin.register(物件)
class 物件(admin.ModelAdmin):
    pass
@admin.register(管理項目)
class 管理項目(admin.ModelAdmin):
    pass
@admin.register(契約)
class 契約(admin.ModelAdmin):
    pass
@admin.register(支払先)
class 支払先(admin.ModelAdmin):
    pass
@admin.register(保証会社)
class 保証会社(admin.ModelAdmin):
    pass


@admin.register(敷金保証金)
class 敷金保証金(admin.ModelAdmin):
    pass

@admin.register(売上)
class 売上(admin.ModelAdmin):
    list_display = ['id', '物件ID', 'テナントID', '管理項目コード', '契約ID', 'レポート日', '請求金額']

@admin.register(費用)
class 費用(admin.ModelAdmin):
    pass

@admin.register(ステータス)
class ステータス(admin.ModelAdmin):
    pass


@admin.register(MonthSelect)
class MonthSelect(admin.ModelAdmin):
    pass

@admin.register(BMItems)
class BMItems(admin.ModelAdmin):
    pass