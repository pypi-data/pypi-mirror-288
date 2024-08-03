__all__ = ["PullQueue"]

import json
from django.db import models


class PullQueue(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=255,unique=True)

    class Meta:
        db_table = "redis_pull_queue"
