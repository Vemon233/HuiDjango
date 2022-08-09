from django.db import models

# Create your models here.
from django.template.defaultfilters import slugify


class Disease(models.Model):
    id = models.CharField(primary_key=True, max_length=7)
    name = models.CharField(max_length=40)
    date = models.DateField(blank=True, null=True)
    country = models.CharField(max_length=20, blank=True, null=True)
    cases = models.IntegerField(blank=True, null=True)
    di_class = models.CharField(db_column='class', max_length=12, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'disease'
