# tests.py
from django.test import TestCase, Client
from django.urls import reverse
from portfolio.models import Portfolio
from django.contrib.auth import get_user_model


class MainViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = get_user_model().objects.create_user(
            email="testuser@example.com",
            password="testpass",
        )
        self.portfolio = Portfolio.objects.create(
            user=self.user,
            slug="testslug",
            about="This is a test portfolio",
        )

    def test_index_view(self):
        response = self.client.get(reverse("main:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/index.html")

    def test_portfolio_detail_view(self):
        response = self.client.get(
            reverse("main:portfolio-detail", kwargs={"slug": self.portfolio.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/portfolio_detail.html")

    def test_gig_detail_view(self):
        response = self.client.get(
            reverse(
                "main:gig-detail",
                kwargs={"slug": self.portfolio.slug, "id": self.portfolio.id},
            )
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/gig_detail.html")

    def test_test_page_view(self):
        self.client.login(email="testuser@example.com", password="testpass")
        response = self.client.get(reverse("main:test-page"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/test-page.html")

    def test_change_theme_view(self):
        response = self.client.get(reverse("main:change-theme"))
        self.assertRedirects(response, "/")

    def test_search_city_view(self):
        response = self.client.get(
            reverse("main:search-city", kwargs={"search": "test city"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/search.html")

    def test_search_view(self):
        response = self.client.get(
            reverse("main:search"), {"autocomplete": "test city, test country"}
        )
        self.assertRedirects(response, "/test city/")
