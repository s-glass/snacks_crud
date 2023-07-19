from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Snack


class MovieTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="tester", email="tester@email.com", password="pass"
        )

        self.snack = Snack.objects.create(
            name="snack1", description="description test", purchaser=self.user,
        )

    def test_string_representation(self):
        self.assertEqual(str(self.snack), "snack1")

    def test_snack_content(self):
        self.assertEqual(f"{self.snack.title}", "snack1")
        self.assertEqual(f"{self.snack.purchaser}", "purchaser")
        self.assertEqual(f"{self.snack.description}", "description test")

    def test_snack_list_view(self):
        response = self.client.get(reverse("list_view"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "snack1")
        self.assertTemplateUsed(response, "snack-list.html")

    def test_snack_detail_view(self):
        response = self.client.get(reverse("snack_detail", args="1"))
        no_response = self.client.get("/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Purchaser: purchaser")
        self.assertTemplateUsed(response, "snack-detail.html")

    def test_snack_create_view(self):
        response = self.client.post(
            reverse("create_view"),
            {
                "name": "Gummy Bears",
                "description": "test",
                "purchaser": self.user.id,
            }, follow=True
        )

        self.assertRedirects(response, reverse("detail_view", args="2"))
        self.assertContains(response, "Details about Gummy Bears")



    def test_snack_update_view_redirect(self):
        response = self.client.post(
            reverse("update_view", args="1"),
            {"title": "Updated title", "purchaser":self.user.id, "description":"new description"}
        )
        self.assertRedirects(response, reverse("detail_view", args="1"))

    def test_snack_delete_view(self):
        response = self.client.get(reverse("delete_view", args="1"))
        self.assertEqual(response.status_code, 200)