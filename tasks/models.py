from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.auth.models import User
from taggit.managers import TaggableManager
from django.utils import timezone


class Task(models.Model):
    class Meta:
        ordering = ['deadline']

    user = models.ForeignKey(User)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, blank=True, null=True)
    object_id = models.PositiveIntegerField(blank=True, null=True)
    content_object = GenericForeignKey('content_type', 'object_id')
    content = models.TextField(verbose_name="תוכן")
    area = models.CharField(blank=True, max_length=250, verbose_name="אזור")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="נוצר")
    deadline = models.DateTimeField(blank=True, verbose_name="דד-ליין", null=True)
    done = models.BooleanField(default=False)

    def __str__(self):
        return self.content[:15] + " עבור " + str(self.content_object)

    @property
    def is_past_due(self):
        return timezone.now() > self.deadline