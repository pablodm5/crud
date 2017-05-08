from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=140)
    start_date = models.DateField()
    end_date = models.DateField()
    picture =  models.ImageField(upload_to='media/courses/pictures')
