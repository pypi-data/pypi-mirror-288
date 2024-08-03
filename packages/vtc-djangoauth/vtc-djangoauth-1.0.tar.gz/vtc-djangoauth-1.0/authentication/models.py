import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Permission, Group
from django.contrib.auth.models import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail



# Define a model manager for User model with no username field.


class CustomUserManager(BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        # Create and save a User with the given email and password.
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **extra_fields):
        # Create and save a regular User with the given email and password.
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        # Create and save a SuperUser with the given email and password.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(email, password, **extra_fields)

# Define a model for User with no username field.


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_(
            'Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    groups = models.ManyToManyField(
        Group, related_name='customuser_groups', blank=True)
    user_permissions = models.ManyToManyField(
        Permission, related_name='customuser_user_permissions', blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        # Return the first_name plus the last_name, with a space in between.
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        # Return the short name for the user.
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        # Send an email to this user.
        send_mail(subject, message, from_email, [self.email], **kwargs)
