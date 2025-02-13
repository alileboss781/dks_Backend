from django.shortcuts import render

# Importations nécessaires pour les permissions et les vues
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import View
from django.http import HttpResponse, HttpResponseForbidden, JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

# Importations des modèles, serializers et permissions
from .models import Ressource, Commentaire
from .serializers import RessourceSerializer, CommentaireSerializer
from .permissions import IsAdminOrModerator  # Assurez-vous que ce fichier existe et est correctement configuré


# RessourceViewSet : CRUD pour Ressource
class RessourceViewSet(viewsets.ModelViewSet):
    queryset = Ressource.objects.all()
    serializer_class = RessourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]  # Seuls les utilisateurs authentifiés peuvent créer/modifier


# CommentaireViewSet : CRUD pour Commentaire
class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


# Enregistrement d'un utilisateur
class RegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            return Response({"error": "Champs manquants"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Nom d'utilisateur déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)


# Authentification de l'utilisateur
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)


# Exemple de vue nécessitant une permission
class PublishResourceView(PermissionRequiredMixin, View):
    permission_required = 'mon_app.can_publish'

    def get(self, request, *args, **kwargs):
        return HttpResponse("Resource published!")


# Création d'une ressource avec vérification du rôle de l'utilisateur
def create_resource(request):
    if not hasattr(request.user, 'role') or request.user.role != 'admin':  # Vérifiez si l'attribut 'role' existe
        return HttpResponseForbidden("You do not have permission to perform this action.")
    # Logique pour créer une ressource
    return HttpResponse("Resource created!")


# Exemple de vue utilisant des permissions personnalisées
class ResourceView(APIView):
    permission_classes = [IsAdminOrModerator]

    def get(self, request, format=None):
        return JsonResponse({"message": "Access granted!"})
