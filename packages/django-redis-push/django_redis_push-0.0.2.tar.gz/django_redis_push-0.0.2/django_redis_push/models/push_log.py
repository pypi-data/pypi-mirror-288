__all__ = ["PushLog"]

import time

from django.db import models

def get_timestamp():
    return int(time.time())

class PushLog(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=255)
    count = models.IntegerField()
    created_at = models.IntegerField(default=get_timestamp)

    class Meta:
        db_table = "redis_push_log"
