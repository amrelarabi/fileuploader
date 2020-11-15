import os
from django.dispatch import receiver
from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from .managers import MembersManager


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/year/month/day/<filename>
    current_date = timezone.now()
    year = current_date.year
    month = current_date.month
    day = current_date.day
    return 'uploads/files/user_{0}/{1}/{2}/{3}/{4}'.format(instance.author.id, year, month, day, filename)


class File(models.Model):
    description = models.CharField(max_length=255, blank=True)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )


class Member(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(upload_to='uploads/avatars', null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MembersManager()

    def __str__(self):
        return self.email


# These two auto-delete files from filesystem when they are unneeded:

@receiver(models.signals.post_delete, sender=File)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=File)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False
