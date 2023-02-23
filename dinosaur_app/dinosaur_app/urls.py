"""dinosaur_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

import dinosaurs.views as views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("accounts/register/", views.register, name="register"),
    path("", views.home, name="home"),
    path("search_results/", views.search_results, name="search_results"),
    path("dinosaur/<int:pk>/", views.dinosaur_detail, name="dinosaur_detail"),
    path("dinosaur/add/", views.add_dinosaur, name="add_dinosaur"),
    path("dinosaur/<int:pk>/edit/", views.edit_dinosaur, name="edit_dinosaur"),
    path("dinosaur/<int:pk>/update/", views.update_dinosaur, name="update_dinosaur"),
    path("dinosaur/<int:pk>/delete/", views.delete_dinosaur, name="delete_dinosaur"),
    path("dinosaur/<int:pk>/image/add/", views.add_image, name="add_image"),
    path("dinosaur/<int:pk>/image/delete/", views.delete_image, name="delete_image"),
    path("dinosaur/<int:pk>/favorite/", views.toggle_favorite, name="toggle_favorite"),
    path("dinosaur/<int:pk>/favorite/add/", views.add_favorite, name="add_favorite"),
    path("favorites/", views.list_favorites, name="list_favorites"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
