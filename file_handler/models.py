from django.db import models


class FileHolder(models.Model):
    file = models.FileField(upload_to='uploads')
