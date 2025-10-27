from tortoise.models import Model
from tortoise import fields

class soleProducts(Model):
    id = fields.BigIntField(pk=True)  # 主键
    item_code = fields.CharField(max_length=255)
    title = fields.CharField(max_length=255)
    scrape_time = fields.DatetimeField(auto_now_add=True)
    url = fields.TextField(null=True)
    status = fields.IntField()
    type = fields.IntField()
    num = fields.CharField(max_length=255)
    initialized = fields.IntField()
    brand = fields.CharField(max_length=255)
    category_id = fields.IntField()
    origin = fields.CharField(max_length=10)

    class Meta:
        table = "sole_products"