from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.http import JsonResponse, HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Ressource, Commentaire
from .serializers import RessourceSerializer, CommentaireSerializer
from .permissions import IsAdminOrModerator


# Vue principale pour afficher la page d'accueil
def index(request):
    return HttpResponse("Bienvenue sur le site de gestion des ressources !")

# ViewSet pour la gestion des Ressources
class RessourceViewSet(viewsets.ModelViewSet):
    queryset = Ressource.objects.all()
    serializer_class = RessourceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Vue pour publier une nouvelle ressource
class PublishResourceView(APIView):
    def post(self, request):
        serializer = RessourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ViewSet pour la gestion des Commentaires
class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

# Vue pour l'enregistrement d'un nouvel utilisateur
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

# Vue pour la connexion d'un utilisateur
class LoginView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({"refresh": str(refresh), "access": str(refresh.access_token)}, status=status.HTTP_200_OK)
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)

# Exemple de vue pour des permissions personnalisées (exclusivement pour Admin ou Moderator)
class ResourceView(APIView):
    permission_classes = [IsAdminOrModerator]

    def get(self, request, format=None):
        return JsonResponse({"message": "Access granted!"})
