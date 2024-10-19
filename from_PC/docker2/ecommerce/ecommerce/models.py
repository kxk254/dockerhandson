from django.db import models
import uuid

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="First name", help_text="Enter a category...")
    slug = models.SlugField(unique=True)
    is_active = models.IntegerField(default=False)
    parent = models.ForeignKey("self", on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Inventory Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

class SeasonalEvents(models.Model):
    id = models.BigAutoField(primary_key=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    name = models.CharField(max_length=100, unique=True)

class Product(models.Model):
    IN_STOCK = "IS"
    OUT_OF_STOCK = "OOS"
    BACKORDERED = "BO"

    STOCK_STATUS = {
        IN_STOCK: "In Stock",
        OUT_OF_STOCK: "Out of sotck",
        BACKORDERED: "Back Ordered"
    }

    pid = models.CharField(max_length=255)
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(unique=True)
    is_digital = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=False)
    stock_status = models.CharField(
        max_length=3,
        choices=STOCK_STATUS,
        default=OUT_OF_STOCK,
        )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    seasonal_event = models.ForeignKey(SeasonalEvents, on_delete=models.SET_NULL, null=True)
    product_type = models.ManyToManyField("ProductType", related_name="product_type")

class ProductLine(models.Model):
    price = models.DecimalField(
        max_digits=5,
        decimal_places=2
        )
    sku = models.UUIDField(default=uuid.uuid4)
    stock_qty = models.IntegerField(default=0)
    is_active = models.IntegerField(default=False)
    order = models.IntegerField()
    weight = models.FloatField()
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    attribute_value = models.ManyToManyField("AttributeValue", related_name="attribute_value")

class ProductImage(models.Model):
    name = models.CharField(max_length=100)
    alternative_text = models.CharField(max_length=100)
    url = models.ImageField()
    order = models.IntegerField()

class ProductType(models.Model):
    name = models.CharField(max_length=100)
    parent = models.ForeignKey("self", on_delete=models.CASCADE)

class Attribute(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)

class AttributeValue(models.Model):
    attribute_value = models.CharField(max_length=100)
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE)

class ProductLine_AttributeValue(models.Model):
    attrbute_value = models.ForeignKey(AttributeValue, on_delete=models.CASCADE)
    product_line = models.ForeignKey(ProductLine, on_delete=models.CASCADE)

class Product_ProductType(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)


class StockControl(models.Model):
    stock_qty = models.IntegerField()
    name = models.CharField(max_length=100)
    stock_product = models.OneToOneField(Product, on_delete=models.CASCADE)

    # def save(self, *args, **kwargs):
    #     # Cleanse the integer field by removing commas
    #     if self.some_integer_field:
    #         # Remove commas and convert to an integer
    #         self.some_integer_field = re.sub(r',', '', self.some_integer_field)
    #         try:
    #             self.some_integer_field = int(self.some_integer_field)
    #         except ValueError:
    #             raise ValueError("The some_integer_field must be a valid integer")

    #     # Automatically slugify the name if the slug is not provided
    #     if not self.slug:
    #         self.slug = slugify(self.name)

    #     super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.name