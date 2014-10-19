from django.utils.translation import get_language_info, ugettext_lazy as _
from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from django.core import files
from . import transform


class UserManager(BaseUserManager):
    def create_user(self, **kwargs):
        if 'email' not in kwargs:
            message = 'Users must have an email address'
            ValueError(message)
        email = kwargs.get('email')
        if 'password' not in kwargs:
            message = 'Users must set a password'
            ValueError(message)
        password = kwargs.get('password')
        user = self.model(
            email=UserManager.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, **kwargs):
        user = self.create_user(**kwargs)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        max_length=225,
        unique=True,
        db_index=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def get_username():
        return self.email

    def get_short_name():
        return self.email

    def __unicode__(self):
        return self.email
        

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    phone_number = models.CharField(max_length=225)
    first_name = models.CharField(max_length=225)
    last_name = models.CharField(max_length=225)

    def __unicode__(self):
        return ' '.join([self.first_name, self.last_name])


class Photo(models.Model):
    # media_id = models.AutoField(primary_key=True)
    description = models.TextField()
    title = models.CharField(max_length=32)
    image = models.ImageField(upload_to='images')

    longitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    latitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)
    altitude = models.DecimalField(max_digits=7, decimal_places=3, null=True)

    def save(self, *args, **kwargs):
        location = transform.get_location(self.image)
        self.longitude = location['longitude']
        self.latitude = location['latitude']
        self.altitude = location['altitude']
        super(Photo, self).save(*args, **kwargs)

    def upload_local_image(self, name, path):
        with open(path, 'rb') as file_:
            self.image.save(name, files.File(file_))

    def __unicode__(self):
        return self.title
