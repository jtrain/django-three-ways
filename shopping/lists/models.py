from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Item(TimeStampedModel):
    name = models.TextField()
    quantity = models.PositiveIntegerField()
    belongs_to = models.ForeignKey('List', on_delete=models.CASCADE)


class List(TimeStampedModel):
    name = models.TextField()
