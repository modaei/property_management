from django.db import models


class Country(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    code = models.CharField(blank=False, null=False, max_length=2, unique=True, db_index=True)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(blank=False, null=False, max_length=50)
    country = models.ForeignKey(Country, null=False, on_delete=models.PROTECT)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)

    def __str__(self):
        return self.name
