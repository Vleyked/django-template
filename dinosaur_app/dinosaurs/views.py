import base64, os
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.conf import settings


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
# def dinosaur_detail(request, pk):
#     dino = get_object_or_404(Dinosaur, pk=pk)
#     images = DinoImage.objects.filter(dinosaur=dino)
#     image_urls = []
#     for image in images:
#         image_urls.append(
#             f"data:{image.content_type};base64,{base64.b64encode(image.image.read()).decode()}"
#         )
#     is_favorited = Favorite.objects.filter(user=request.user, dinosaur=dino).exists()
#     return render(
#         request,
#         "dinosaur_detail.html",
#         {"dino": dino, "image_urls": image_urls, "is_favorited": is_favorited},
#     )
def dinosaur_detail(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    images = DinoImage.objects.filter(dinosaur=dino)
    image_urls = []
    for image in images:
        image_path = os.path.join(settings.MEDIA_ROOT, str(image.image))
        with open(image_path, "rb") as f:
            image_data = f.read()
            image_base64 = base64.b64encode(image_data).decode()
            image_url = f"data:image/jpeg;base64,{image_base64}"
            image_urls.append(image_url)
    return render(
        request,
        "dinosaur_detail.html",
        {"dino": dino, "images": images, "image_urls": image_urls},
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
def search_results(request):
    query = request.GET.get("q")
    print(
        query
    )  # Add this line to check that the search query is being retrieved correctly
    if query:
        dinosaurs = Dinosaur.objects.filter(name__icontains=query)
    else:
        dinosaurs = Dinosaur.objects.all()
    return render(request, "search_results.html", {"dinosaurs": dinosaurs})


@login_required
def edit_dinosaur(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    if request.method == "POST":
        form = DinosaurForm(request.POST, request.FILES, instance=dino)
        if form.is_valid():
            form.save()
            return redirect("dinosaur_detail", pk=dino.pk)
    else:
        form = DinosaurForm(instance=dino)
    return render(request, "dinosaur_edit.html", {"form": form, "dino": dino})


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
    dinosaur = get_object_or_404(Dinosaur, pk=pk)
    if request.method == "POST":
        form = DinoImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.dinosaur = dinosaur
            image.save()
            return redirect("dinosaur_detail", pk=dinosaur.pk)
    else:
        form = DinoImageForm()
    return render(request, "add_image.html", {"form": form, "dinosaur": dinosaur})


@login_required
@require_http_methods(["POST"])
def delete_image(request, pk):
    dino_image = get_object_or_404(DinoImage, pk=pk)
    dinosaur_pk = dino_image.dinosaur.pk
    dino_image.delete()
    return redirect("dinosaur_detail", pk=dinosaur_pk)


@login_required
@require_http_methods(["POST"])
def toggle_favorite(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, dinosaur=dino)
    if not created:
        fav.delete()
    return JsonResponse({"success": True, "is_favorited": not created})


@login_required
def add_favorite(request, pk):
    dino = get_object_or_404(Dinosaur, pk=pk)
    fav, created = Favorite.objects.get_or_create(user=request.user, dinosaur=dino)
    if created:
        messages.success(request, "Added to favorites.")
    else:
        messages.error(request, "This dinosaur is already in your favorites.")
    return redirect("dinosaur_detail", pk=dino.pk)


@login_required
def list_favorites(request):
    favorites = Favorite.objects.filter(user=request.user)
    dinos = [fav.dinosaur for fav in favorites]
    return render(request, "list_favorites.html", {"dinos": dinos})
