from django.db import models

# Create your models here.

class Car(models.Model):
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    isElectric = models.BooleanField()

    def __str__(self):
        return self.make