from django.http import JsonResponse, HttpResponse
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from .models import Ressource, Commentaire, User  # Assurez-vous d'importer le modèle User personnalisé
from .serializers import RessourceSerializer, CommentaireSerializer
from .permissions import IsAdminOrModerator

from rest_framework import generics, permissions
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated




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
    permission_classes = [IsAuthenticatedOrReadOnly]  # Permet de publier si l'utilisateur est authentifié

    def post(self, request):
        user = request.user  # Utilisateur actuellement connecté
        serializer = RessourceSerializer(data=request.data)
        if serializer.is_valid():
            # L'utilisateur est associé à la ressource
            serializer.save(auteur=user)  # Vous pouvez adapter selon votre modèle Ressource
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet pour la gestion des Commentaires
class CommentaireViewSet(viewsets.ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class PublishCommentView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request):
        user = request.user
        if not user or user.is_anonymous:
            return Response({"error": "Utilisateur non authentifié"}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = CommentaireSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save(auteur=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# Vue pour l'enregistrement d'un nouvel utilisateur
class RegisterView(APIView):
    permission_classes = [AllowAny]  # Tout le monde peut accéder à cette vue

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        role = request.data.get("role", "user")  # Par défaut, le rôle est 'user'

        # Vérification de la présence des champs nécessaires
        if not username or not password:
            return JsonResponse({"error": "Champs manquants"}, status=status.HTTP_400_BAD_REQUEST)

        # Vérification si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "Nom d'utilisateur déjà utilisé"}, status=status.HTTP_400_BAD_REQUEST)

        # Validation du mot de passe
        try:
            validate_password(password)
        except ValidationError as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Création de l'utilisateur
        try:
            user = User.objects.create_user(username=username, password=password, role=role)
            return JsonResponse({"message": "Utilisateur créé avec succès"}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vue pour la connexion d'un utilisateur
class LoginView(APIView):
    permission_classes = [AllowAny]  # Accès ouvert à cette vue

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            # Création du token JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Identifiants invalides"}, status=status.HTTP_401_UNAUTHORIZED)


# Exemple de vue pour des permissions personnalisées (exclusivement pour Admin ou Moderator)
class ResourceView(APIView):
    permission_classes = [IsAdminOrModerator]  # Seulement accessible aux admins et modérateurs

    def get(self, request, format=None):
        return JsonResponse({"message": "Access granted!"})
    

# Permission personnalisée pour gérer la suppression
class IsOwnerOrModeratorOrAdmin(permissions.BasePermission):
    """
    Permission pour autoriser uniquement le propriétaire, un modérateur ou un administrateur à supprimer un objet.
    """

    def has_object_permission(self, request, view, obj):
        # Les administrateurs et modérateurs peuvent tout supprimer
        if request.user.is_staff or request.user.is_superuser:
            return True
        # Seul l'auteur peut supprimer son propre contenu
        return obj.auteur == request.user
    
# class DeleteCommentView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, comment_id):
#         commentaire = get_object_or_404(Commentaire, id=comment_id)

#         # Vérifie si l'utilisateur est l'auteur ou un modérateur/admin
#         if request.user == commentaire.auteur or request.user.is_staff or request.user.is_superuser:
#             commentaire.delete()
#             return Response({"message": "Commentaire supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({"error": "Vous n'avez pas la permission de supprimer ce commentaire"}, status=status.HTTP_403_FORBIDDEN)
        

# class DeleteResourceView(APIView):
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, resource_id):
#         ressource = get_object_or_404(Ressource, id=resource_id)

#         # Vérifie si l'utilisateur est l'auteur ou un modérateur/admin
#         if request.user == ressource.auteur or request.user.is_staff or request.user.is_superuser:
#             ressource.delete()
#             return Response({"message": "Ressource supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
#         else:
#             return Response({"error": "Vous n'avez pas la permission de supprimer cette ressource"}, status=status.HTTP_403_FORBIDDEN)


#Vue pour supprimer un commentaire
# class DeleteCommentView(generics.DestroyAPIView):
#     queryset = Commentaire.objects.all()
#     serializer_class = CommentaireSerializer
#     permission_classes = [IsOwnerOrModeratorOrAdmin]

#     def delete(self, request, *args, **kwargs):
#         commentaire = get_object_or_404(Commentaire, id=kwargs["pk"])
#         self.check_object_permissions(request, commentaire)
#         commentaire.delete()
#         return Response({"message": "Commentaire supprimé avec succès."}, status=status.HTTP_204_NO_CONTENT)


class DeleteCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        comment_id = request.data.get("comment_id")  # Récupérer l'ID dans le body

        if not comment_id:
            return Response({"error": "L'ID du commentaire est requis"}, status=status.HTTP_400_BAD_REQUEST)

        commentaire = get_object_or_404(Commentaire, id=comment_id)

        if request.user == commentaire.auteur or request.user.is_staff or request.user.is_superuser:
            commentaire.delete()
            return Response({"message": "Commentaire supprimé avec succès"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Vous n'avez pas la permission de supprimer ce commentaire"}, status=status.HTTP_403_FORBIDDEN)



# Vue pour supprimer une ressource
# class DeleteResourceView(generics.DestroyAPIView):
#     queryset = Ressource.objects.all()
#     serializer_class = RessourceSerializer
#     permission_classes = [IsOwnerOrModeratorOrAdmin]

#     def delete(self, request, *args, **kwargs):
#         ressource = get_object_or_404(Ressource, id=kwargs["pk"])
#         self.check_object_permissions(request, ressource)
#         ressource.delete()
#         return Response({"message": "Ressource supprimée avec succès."}, status=status.HTTP_204_NO_CONTENT)


class DeleteResourceView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        resource_id = request.data.get("resource_id")  # Récupérer l'ID dans le body

        if not resource_id:
            return Response({"error": "L'ID de la ressource est requis"}, status=status.HTTP_400_BAD_REQUEST)

        ressource = get_object_or_404(Ressource, id=resource_id)

        if request.user == ressource.auteur or request.user.is_staff or request.user.is_superuser:
            ressource.delete()
            return Response({"message": "Ressource supprimée avec succès"}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Vous n'avez pas la permission de supprimer cette ressource"}, status=status.HTTP_403_FORBIDDEN)
