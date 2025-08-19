from django.utils import timezone
from django.db import models
from django.urls import reverse


class Feedback(models.Model):
    subject = models.CharField(max_length=255)
    rate = models.PositiveSmallIntegerField()
    message = models.TextField()


    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('feedback_detail', kwargs={'pk': self.pk})

