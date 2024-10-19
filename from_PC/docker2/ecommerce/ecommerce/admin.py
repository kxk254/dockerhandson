from django.contrib import admin
from ecommerce.models import Category, Product, ProductType, ProductLine

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ['name', 'slug']
    list_display_links =('id',)
    list_editable = ('name',)


class ProductLineInLine(admin.StackedInLine):
    model = ProductLine
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    list_filter = ("stock_status",)
    inlines = [ProductLineInLine]



admin.site.register(Category, CategoryAdmin)
admin.site.register(Product)