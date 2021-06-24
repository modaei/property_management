from django.conf import settings
from django.db import models
from properties.models import Property
from property_management.validators import validate_names, validate_phone_number


class Tenant(models.Model):
    email = models.EmailField(unique=True, blank=True, null=True, db_index=True)
    first_name = models.CharField(max_length=255, blank=False, null=False, validators=[validate_names])
    last_name = models.CharField(max_length=255, blank=False, null=False, validators=[validate_names])
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=20,
                                    validators=[validate_phone_number])
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, null=False, on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            return f'{self.first_name} {self.last_name}'
        else:
            return None


class Lease(models.Model):
    property = models.ForeignKey(Property, null=False, on_delete=models.PROTECT)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    deposit = models.PositiveIntegerField()
    rent = models.PositiveIntegerField()
    tenant = models.ForeignKey(Tenant, null=False, on_delete=models.PROTECT)
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True, verbose_name="Created")
    update_date = models.DateTimeField(auto_now=True, auto_now_add=False, verbose_name="Last updated")

