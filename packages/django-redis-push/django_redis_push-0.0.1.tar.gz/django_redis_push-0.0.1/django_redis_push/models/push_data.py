__all__ = ["PushData"]

import json
from django.db import models


class PushData(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=255)
    data = models.JSONField()

    class Meta:
        db_table = "redis_push_data"

    def get_data(self):
        return json.loads(self.data)
