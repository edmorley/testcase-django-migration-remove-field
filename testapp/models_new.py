from django.db import models


class Push(models.Model):
    repository = models.PositiveIntegerField()
    revision = models.CharField(max_length=40)

    class Meta:
        unique_together = [
            ('repository', 'revision'),
        ]
