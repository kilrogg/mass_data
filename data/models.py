from django.db import models

# Create your models here.


class TestData(models.Model):

    belegnr = models.CharField(max_length=30, primary_key=True)
    text = models.TextField(blank=False)


