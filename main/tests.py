from django.test import TestCase, Client


class My404ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_rendering_404_template(self):
        response = self.client.get("/not-a-valid-url/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "main/404.html")


class AboutUsTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_rendering_about_us_template(self):
        response = self.client.get("/about/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "main/about-us.html")
