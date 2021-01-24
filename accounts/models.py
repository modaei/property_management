from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from .validators import validate_phone_number, validate_names


class UserManager(BaseUserManager):
    def create_user(self, email, phone_number, password=None, is_active=True, is_staff=False,
                    is_admin=False):
        user_obj = self.model(
            email=email,
            phone_number=phone_number
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(self._db)
        return user_obj

    def create_staff_user(self, email, password):
        user_obj = self.create_user(
            email=email,
            phone_number=None,
            password=password,
            is_staff=True,
        )
        return user_obj

    def create_superuser(self, email, password):
        user_obj = self.create_user(
            email=email,
            phone_number=None,
            password=password,
            is_staff=True,
            is_admin=True,
        )
        return user_obj


class User(AbstractBaseUser):
    email = models.EmailField(unique=True, blank=False, null=False, db_index=True)
    active = models.BooleanField(default=True)  # Can login
    staff = models.BooleanField(default=False)  # Staff members
    admin = models.BooleanField(default=False)  # Superuser
    first_name = models.CharField(max_length=255, blank=False, null=False, validators=[validate_names])
    last_name = models.CharField(max_length=255, blank=False, null=False, validators=[validate_names])
    email_verified = models.BooleanField(blank=False, null=False, default=False)
    phone_number = models.CharField(unique=True, blank=True, null=True, max_length=20,
                                    validators=[validate_phone_number])
    phone_number_verified = models.BooleanField(blank=False, null=False, default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        old = type(self).objects.get(pk=self.pk) if self.pk else None
        if old and old.phone_number != self.phone_number:
            self.phone_number_verified = False
        super(User, self).save(*args, **kwargs)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def short_name(self):
        return self.first_name

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def is_active(self):
        return self.active

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin


class ValidationToken(models.Model):
    VALIDATION_TYPES = (
        ('email', 'email'),
        ('phone', 'phone')
    )
    PHONE_EXPIRY_INTERVAL = timedelta(minutes=5)
    EMAIL_EXPIRY_INTERVAL = timedelta(hours=12)

    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE)
    token = models.CharField(max_length=120, null=False)
    validation_type = models.CharField(max_length=20, choices=VALIDATION_TYPES, null=False, default='email')
    create_date = models.DateTimeField(auto_now=False, auto_now_add=True)

    @property
    def is_expired(self):
        if self.validation_type == 'email':
            return self.create_date + self.EMAIL_EXPIRY_INTERVAL < timezone.now()
        elif self.validation_type == 'phone':
            return self.create_date + self.PHONE_EXPIRY_INTERVAL < timezone.now()
