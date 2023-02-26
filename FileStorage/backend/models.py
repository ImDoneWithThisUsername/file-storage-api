from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
import os
def upload_to(instance, filename):
    return 'user_images/{}/{}'.format(instance.user_id, filename)

class CustomUser(AbstractUser):
    public_key = models.IntegerField(null=True)
    n = models.IntegerField(null=True)
    def __str__(self) -> str:
        return self.username

class Image(models.Model):
    image = models.ImageField(upload_to=upload_to)
    user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.CASCADE)
    encrypted_session_key = models.IntegerField(null=True, blank=True)
    def __str__(self) -> str:
        return os.path.basename(self.image.name)

