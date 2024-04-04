from django.db import models
from datetime import date
from django.contrib.auth.models import User

# Create your models here.
FUELS = (
    ('R', 'Regular'),
    ('P', 'Premium'),
    ('S', 'Supreme'),
    ('E', 'Electric')
)

class Accessory(models.Model):
    name = models.CharField(max_length=20)
    color= models.CharField(max_length=15)

    def __str__(self):
        return f'{self.name}'

class Car(models.Model):
    make = models.CharField(max_length=20)
    model = models.CharField(max_length=20)
    year = models.IntegerField()
    isElectric = models.BooleanField()
    accessories = models.ManyToManyField(Accessory)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.make
    
    # def fueled_for_today(self):
    #     return self.fueling_set.filter(date=date.today()).count() >= len(FUELS)
    
class Fueling(models.Model):
    date = models.DateField('Fueling Date')
    fuelType = models.CharField(max_length=1, choices=FUELS, default=FUELS[0][0])
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.get_fuelType_display()} on {self.date}'
    
    class Meta:
        ordering = ['-date']