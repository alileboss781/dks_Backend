from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import UserManager

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    objects = UserManager()



class UserManager(BaseUserManager):
    def create_user(self, username, password=None, role='user', **extra_fields):
        if not username:
            raise ValueError("Le nom d'utilisateur doit être fourni")
        user = self.model(username=username, role=role, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, role='admin', **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, role, **extra_fields)



class Ressource(models.Model):
    titre = models.CharField(max_length=255)
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.titre

    class Meta:
        verbose_name = "Ressource"
        verbose_name_plural = "Ressources"

class Commentaire(models.Model):
    contenu = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='reponses')  # Permettre les réponses

    def __str__(self):
        return f"Commentaire par {self.auteur.username} sur {self.ressource.titre}"

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"

