from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class Dinosaur(models.Model):
    TINY = "tiny"
    VERY_SMALL = "very_small"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"
    VERY_LARGE = "very_large"

    SIZE_CHOICES = [
        (TINY, _("Tiny")),
        (VERY_SMALL, _("Very Small")),
        (SMALL, _("Small")),
        (MEDIUM, _("Medium")),
        (LARGE, _("Large")),
        (VERY_LARGE, _("Very Large")),
    ]

    HERBIVORE = "herbivore"
    CARNIVORE = "carnivore"
    OMNIVORE = "omnivore"

    EATING_CHOICES = [
        (HERBIVORE, _("Herbivore")),
        (CARNIVORE, _("Carnivore")),
        (OMNIVORE, _("Omnivore")),
    ]

    name = models.CharField(max_length=255)
    period = models.CharField(max_length=50)
    size = models.CharField(max_length=20, choices=SIZE_CHOICES)
    eating = models.CharField(max_length=20, choices=EATING_CHOICES)
    color = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("dinosaur_detail", args=[str(self.pk)])


class DinoImage(models.Model):
    dinosaur = models.ForeignKey(Dinosaur, on_delete=models.CASCADE)
    image = models.FileField(upload_to="dinosaur_images/")

    def __str__(self):
        return self.image.name


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dinosaur = models.ForeignKey(Dinosaur, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("user", "dinosaur")

    def __str__(self):
        return f"{self.user.username} likes {self.dinosaur.name}"
