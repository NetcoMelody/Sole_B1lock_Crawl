from tortoise.models import Model
from tortoise import fields

class productPrice_api_log(Model):
    id = fields.IntField(pk=True)  # 主键
    userName = fields.CharField(max_length=255)
    data = fields.JSONField()
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "stockX_productPrice_api_log"