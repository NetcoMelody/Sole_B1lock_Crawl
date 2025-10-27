from tortoise.models import Model
from tortoise import fields

class sizeCharts(Model):
    id = fields.IntField(pk=True)  # 主键
    variation_id = fields.CharField(max_length=100)
    sku = fields.CharField(max_length=50)
    us_M_size = fields.CharField(max_length=100)
    us_W_size = fields.CharField(max_length=100)
    us_size = fields.CharField(max_length=100)
    uk_size = fields.CharField(max_length=100)
    cm_size = fields.CharField(max_length=100)
    kr_size = fields.CharField(max_length=100)
    eu_size = fields.CharField(max_length=100)
    msg = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    product_id = fields.CharField(max_length=255)
    fee = fields.DecimalField(10,2)

    class Meta:
        table = "stockX_sizeCharts"