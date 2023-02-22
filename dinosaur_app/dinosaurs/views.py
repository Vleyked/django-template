from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseBadRequest, JsonResponse
from .models import Dinosaur, DinoImage, Favorite
from .forms import DinosaurForm, DinoImageForm


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!")
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/register.html", {"form": form})


def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"You are now logged in as {user.username}")
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("home")


@login_required
def home(request):
    dinos = Dinosaur.objects.all()
    return render(request, "home.html", {"dinos": dinos})


@login_required
def dinosaur_detail(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    images = DinoImage.objects.filter(dinosaur=dino)
    is_favorited = Favorite.objects.filter(user=request.user, dinosaur=dino).exists()
    return render(
        request,
        "dinosaur_detail.html",
        {"dino": dino, "images": images, "is_favorited": is_favorited},
    )


@login_required
def add_dinosaur(request):
    if request.method == "POST":
        form = DinosaurForm(request.POST, request.FILES)
        if form.is_valid():
            dino = form.save()
            messages.success(request, f"{dino.name} has been added to the database!")
            return redirect("dinosaur_detail", pk=dino.pk)
    else:
        form = DinosaurForm()
    return render(request, "add_dinosaur.html", {"form": form})


@login_required
def update_dinosaur(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    if request.method == "POST":
        form = DinosaurForm(request.POST, request.FILES, instance=dino)
        if form.is_valid():
            dino = form.save()
            messages.success(request, f"{dino.name} has been updated!")
            return redirect("dinosaur_detail", pk=dino.pk)
    else:
        form = DinosaurForm(instance=dino)
    return render(request, "add_dinosaur.html", {"form": form})


@login_required
def delete_dinosaur(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    if request.method == "POST":
        dino.delete()
        messages.success(request, f"{dino.name} has been deleted from the database!")
        return redirect("home")
    return render(request, "delete_dinosaur.html", {"dino": dino})


@login_required
@require_http_methods(["POST"])
def add_image(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    form = DinoImageForm(request.POST, request.FILES)
    if form.is_valid():
        image = form.save(commit=False)
        image.dinosaur = dino
        image.save()
        messages.success(request, "Image added!")
        return JsonResponse({"success": True, "img_url": image.image.url})
    else:
        return JsonResponse({"success": False, "errors": form.errors})


@login_required
@require_http_methods(["POST"])
def delete_image(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    image_id = request.POST.get("image_id")
    image = get_object_or_404(DinoImage, pk=image_id, dinosaur=dino)
    image.delete()
    messages.success(request, "Image deleted!")
    return JsonResponse({"success": True})


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, dinosaur=dino)
    if not created:
        fav.delete()
    return JsonResponse({"success": True, "is_favorited": not created})


@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    dinos = [fav.dinosaur for fav in favorites]
    return render(request, "list_favorites.html", {"dinos": dinos})
