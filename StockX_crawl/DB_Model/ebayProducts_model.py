from tortoise.models import Model
from tortoise import fields

class ebayProducts(Model):
    id = fields.BigIntField(pk=True)  # 主键
    title = fields.TextField()
    variation = fields.TextField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=255)
    scrape_time = fields.DatetimeField(auto_now_add=True)
    stock = fields.IntField()
    version = fields.CharField(max_length=255)
    wrong = fields.BooleanField()
    orig_data = fields.JSONField()
    sql_id = fields.IntField()
    product_id = fields.TextField()

    class Meta:
        table = "ebay_product_variations"
