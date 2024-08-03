__all__ = ["PullData"]

import json
from django.db import models


class PullData(models.Model):
    id = models.BigAutoField(primary_key=True)
    queue = models.CharField(max_length=255)
    data = models.JSONField()

    class Meta:
        db_table = "redis_pull_data"
        indexes = [
            models.Index(
                fields=[
                    "queue",
                ]
            ),
        ]

    def get_data(self):
        return json.loads(self.data)
