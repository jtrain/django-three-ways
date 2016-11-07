from django.db import models
from django.urls.base import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Item(TimeStampedModel):
    name = models.TextField()
    quantity = models.PositiveIntegerField()
    belongs_to = models.ForeignKey('List', on_delete=models.CASCADE,
                                   related_name='items')


class List(TimeStampedModel):
    name = models.TextField()

    def get_absolute_url(self):
        return reverse('list-detail', kwargs={"pk": self.id})
