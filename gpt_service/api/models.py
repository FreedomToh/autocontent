import logging
import uuid

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

nb = dict(null=True, blank=True)


class CreateTracker(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        abstract = True
        ordering = ('-created_at',)


class CreateUpdateTracker(CreateTracker):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta(CreateTracker.Meta):
        abstract = True
        db_table = "gpt_users"


class GetOrNoneManager(models.Manager):
    """returns none if object doesn't exist else model instance"""
    def get_or_none(self, **kwargs):
        try:
            return self.get(**kwargs)
        except ObjectDoesNotExist:
            return None


class User(CreateUpdateTracker):
    user_id = models.PositiveBigIntegerField(primary_key=True)
    username = models.CharField(max_length=32, **nb)
    # first_name = models.CharField(max_length=256)
    # last_name = models.CharField(max_length=256, **nb)
    language_code = models.CharField(max_length=8, help_text="Telegram client's lang", **nb)
    # deep_link = models.CharField(max_length=64, **nb)

    # is_blocked_bot = models.BooleanField(default=False)

    is_admin = models.BooleanField(default=False)

    # objects = GetOrNoneManager()  # user = User.objects.get_or_none(user_id=<some_id>)
    # admins = AdminUserManager()  # User.admins.all()

    def __str__(self):
        return f'{self.username}' if self.username is not None else f'{self.user_id}'

    @classmethod
    def create_user(cls):
        logging.info("Creating user")

        new_id = 0
        if cls.objects.count() > 0:
            new_id = cls.objects.all().order_by("-user_id").first().user_id + 1

        obj = cls(user_id=new_id)
        obj.save()
        return obj


class DialogsModel(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    gpt_tokens = models.IntegerField(default=0)
