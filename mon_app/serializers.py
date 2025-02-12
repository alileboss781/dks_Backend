from rest_framework import serializers
from .models import Ressource, Commentaire
from django.contrib.auth.models import User

class RessourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ressource
        fields = '__all__'  # Inclure tous les champs du modèle Ressource

class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = '__all__'  # Inclure tous les champs du modèle Commentaire

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
