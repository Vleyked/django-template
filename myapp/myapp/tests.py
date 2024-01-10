from django.test import TestCase
from django.urls import reverse
from .models import Dinosaur, DinoImage, Favorite
from django.contrib.auth.models import User


class DinosaurViewsTestCase(TestCase):
    @classmethod
    def set_up_test_data(cls):
        # Create a test user
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="password"
        )

        # Create some test dinosaurs
        cls.dinosaur1 = Dinosaur.objects.create(
            name="Tyrannosaurus",
            period="Cretaceous",
            size="large",
            eating="carnivore",
            color="brown",
            description="A giant meat-eating dinosaur",
            added_by=cls.user,
        )
        cls.dinosaur2 = Dinosaur.objects.create(
            name="Triceratops",
            period="Cretaceous",
            size="large",
            eating="herbivore",
            color="green",
            description="A large, horned dinosaur",
            added_by=cls.user,
        )

    def test_home_view(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dinosaur1.name)
        self.assertContains(response, self.dinosaur2.name)

    def test_dinosaur_detail_view(self):
        response = self.client.get(reverse("dinosaur_detail", args=[self.dinosaur1.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dinosaur1.name)
        self.assertContains(response, self.dinosaur1.period)

    def test_add_dinosaur_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("add_dinosaur"),
            {
                "name": "Stegosaurus",
                "period": "Jurassic",
                "size": "large",
                "eating": "herbivore",
                "color": "green",
                "description": "A large, plated dinosaur",
                "image1": "test_image.jpg",
                "image2": "test_image.jpg",
                "image3": "test_image.jpg",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dinosaur.objects.count(), 3)

    def test_delete_dinosaur_view(self):
        self.client.login(username="testuser", password="password")
        response = self.client.post(
            reverse("delete_dinosaur", args=[self.dinosaur1.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Dinosaur.objects.count(), 1)
        self.assertFalse(Dinosaur.objects.filter(pk=self.dinosaur1.pk).exists())


class UserViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a test user
        cls.user = User.objects.create_user(
            username="testuser", email="testuser@example.com", password="testpassword"
        )

    def test_login_view(self):
        # Test login view with GET request
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/login.html")

        # Test login view with POST request
        response = self.client.post(
            reverse("login"), {"username": "testuser", "password": "testpassword"}
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_logout_view(self):
        # Test logout view
        self.client.force_login(self.user)
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_register_view(self):
        # Test register view with GET request
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "registration/register.html")

        # Test register view with POST request
        response = self.client.post(
            reverse("register"),
            {
                "username": "testuser2",
                "email": "testuser2@example.com",
                "password1": "testpassword2",
                "password2": "testpassword2",
            },
        )
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("home"))

    def test_list_favorites_view(self):
        # Test list favorites view when user is not logged in
        response = self.client.get(reverse("list_favorites"))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response, f"{reverse('login')}?next={reverse('list_favorites')}"
        )

        # Test list favorites view when user is logged in
        self.client.force_login(self.user)
        response = self.client.get(reverse("list_favorites"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "list_favorites.html")

    def test_add_favorite_view(self):
        # Test add favorite view when user is not logged in
        dinosaur = Dinosaur.objects.create(
            name="Test Dinosaur",
            period="triassic",
            size="medium",
            eating="herbivore",
            color="green",
            description="A test dinosaur",
            user=self.user,
        )
        response = self.client.get(reverse("add_favorite", args=[dinosaur.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('add_favorite', args=[dinosaur.id])}",
        )

        # Test add favorite view when user is logged in
        self.client.force_login(self.user)
        response = self.client.get(reverse("add_favorite", args=[dinosaur.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_favorites"))

    def test_delete_favorite_view(self):
        # Test delete favorite view when user is not logged in
        dinosaur = Dinosaur.objects.create(
            name="Test Dinosaur",
            period="triassic",
            size="medium",
            eating="herbivore",
            color="green",
            description="A test dinosaur",
            user=self.user,
        )
        response = self.client.get(reverse("delete_favorite", args=[dinosaur.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(
            response,
            f"{reverse('login')}?next={reverse('delete_favorite', args=[dinosaur.id])}",
        )

        # Test delete favorite view when user is logged in
        self.client.force_login(self.user)
        response = self.client.get(reverse("delete_favorite", args=[dinosaur.id]))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse("list_favorites"))
