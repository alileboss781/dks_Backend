from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def __str__(self):
        return self.username
class Resource(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        permissions = [
            ("can_publish", "Can publish resources"),
            ("can_moderate", "Can moderate comments"),
        ]
