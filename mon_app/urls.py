from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Créer un routeur pour les ViewSets
router = DefaultRouter()
router.register(r'ressources', views.RessourceViewSet, basename='ressource')  # Ressources
router.register(r'commentaires', views.CommentaireViewSet, basename='commentaire')  # Commentaires

urlpatterns = [
    # Routes pour l'inscription et la connexion
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),

    # Exemple de route pour les permissions personnalisées
    path('publish/', views.PublishResourceView.as_view(), name='publish_resource'),

    # Routes API générées automatiquement pour les ViewSets
    path('api/', include(router.urls)),

    # Autres endpoints API ou vues supplémentaires si nécessaire
]
