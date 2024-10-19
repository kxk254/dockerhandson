from django.contrib import admin
from .models import Broker, UpdateReport

# Register your models here.
@admin.register(Broker)
class Broker(admin.ModelAdmin):
    pass

@admin.register(UpdateReport)
class UpdateReport(admin.ModelAdmin):
    pass

