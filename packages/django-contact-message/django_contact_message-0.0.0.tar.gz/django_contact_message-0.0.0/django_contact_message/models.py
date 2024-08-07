__all__ = [
    "Message",
]

import time

from django.conf import settings
from django.db import models

def get_timestamp():
    return int(time.time())

class Message(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,null=True,on_delete=models.DO_NOTHING)
    email = models.TextField()
    subject = models.TextField()
    message = models.TextField()
    created_at = models.IntegerField(default=get_timestamp)

    class Meta:
        db_table = "django_contact_message"
        ordering = ("-created_at",'id')

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = int(time.time())
        super().save(*args, **kwargs)
