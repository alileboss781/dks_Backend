# mon_app/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Créer un routeur pour les ViewSets
router = DefaultRouter()
router.register(r'ressources', views.RessourceViewSet, basename='ressource')
router.register(r'commentaires', views.CommentaireViewSet, basename='commentaire')

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('publish/', views.PublishResourceView.as_view(), name='publish_resource'),
    path('api/', include(router.urls)),
     #Route d'index pour l'application
    
]





