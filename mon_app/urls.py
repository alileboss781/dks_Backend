from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views  # Importer les vues

# Créer un routeur pour les ViewSets
router = DefaultRouter()
router.register(r'ressources', views.RessourceViewSet)  # Route pour les ressources
router.register(r'commentaires', views.CommentaireViewSet)  # Route pour les commentaires

urlpatterns = [
    # Routes pour l'inscription et la connexion
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),

    # Inclure les URLs générées automatiquement pour les viewsets
    path('api/', include(router.urls)),  # Les routes pour les viewsets de ressources et commentaires
]

