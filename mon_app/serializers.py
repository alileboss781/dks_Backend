from rest_framework import serializers
from .models import Ressource, Commentaire
from django.contrib.auth.models import User
from django.utils.timesince import timesince


class UserSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else "Nom complet indisponible"



class CommentaireSerializer(serializers.ModelSerializer):
    reponses = serializers.SerializerMethodField()  # Champ pour afficher les réponses
    time_since_creation = serializers.SerializerMethodField()  # Champ pour afficher le temps écoulé

    class Meta:
        model = Commentaire
        fields = ['id', 'contenu', 'date_creation', 'auteur', 'ressource', 'parent', 'reponses', 'time_since_creation']

    def get_reponses(self, obj):
        """Retourne les réponses associées au commentaire."""
        reponses = obj.reponses.all()  # Récupérer toutes les réponses
        return CommentaireSerializer(reponses, many=True).data if reponses.exists() else []

    def get_time_since_creation(self, obj):
        """Retourne le temps écoulé depuis la création."""
        return timesince(obj.date_creation)



class RessourceSerializer(serializers.ModelSerializer):
    commentaires = CommentaireSerializer(many=True, read_only=True)

    class Meta:
        model = Ressource
        fields = '__all__'

    def validate_titre(self, value):
        if Ressource.objects.filter(titre=value).exists():
            raise serializers.ValidationError("Une ressource avec ce titre existe déjà.")
        return value


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data.get('email', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
