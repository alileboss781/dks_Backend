from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('moderator', 'Moderator'),
        ('user', 'User'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')



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
    ressource = models.ForeignKey(Ressource, on_delete=models.CASCADE, related_name='commentaires')
    auteur = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Commentaire par {self.auteur.username} sur {self.ressource.titre}"

    class Meta:
        verbose_name = "Commentaire"
        verbose_name_plural = "Commentaires"
