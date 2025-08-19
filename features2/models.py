from django.db import models

class MyFormModel(models.Model):
    file = models.FileField(upload_to='uploads/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_url = models.URLField(blank=True, null=True)



