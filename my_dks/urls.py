"""
URL configuration for my_dks project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# my_dks/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from mon_app import views
from rest_framework.routers import DefaultRouter
from mon_app.views import DeleteCommentView, DeleteResourceView




urlpatterns = [
    path('', views.index, name='index'),  # Page d'accueil
    path('admin/', admin.site.urls),

    # Routes d'authentification JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Inclure les routes de l'application mon_app
    path('api/', include('mon_app.urls')),  # Remarquez que cela inclut mon_app.urls
    path('register/', views.RegisterView.as_view(), name='register'),
    path("api/register/", views.RegisterView.as_view(), name="register"),

    path('login/', views.LoginView.as_view(), name='login'),
    path('publish/', views.PublishResourceView.as_view(), name='publish_resource'),
    path('publish-comment/', views.PublishCommentView.as_view(), name='publish_comment'),
     path('api/publish-comment/', views.PublishCommentView.as_view(), name='publish_comment'),
   # path('api/', include(router.urls)),

   path('api/delete-comment/', DeleteCommentView.as_view(), name='delete-comment'),
   path('api/delete-resource/', DeleteResourceView.as_view(), name='delete-resource'),
]



