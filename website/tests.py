from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from website.models import Costumer


class RecordAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model().objects
        cls.owner = users.create_superuser("owner", password="synthetic-test-password")
        cls.staff = users.create_user("staff", is_staff=True)
        cls.record = Costumer.objects.create(first_name="Synthetic", last_name="Customer")

    def test_anonymous_cannot_read_records_or_register(self):
        self.assertRedirects(self.client.get(reverse("home")), "/login/?next=/")
        self.assertEqual(self.client.get("/register/").status_code, 404)

    def test_staff_needs_a_model_permission(self):
        self.client.force_login(self.staff)
        self.assertEqual(self.client.get(reverse("home")).status_code, 403)
        self.staff.user_permissions.add(
            Permission.objects.get(content_type__app_label="website", codename="view_costumer")
        )
        self.assertContains(self.client.get(reverse("home")), "Synthetic Customer")
        for name in ("update_costumer", "delete_costumer"):
            self.assertEqual(
                self.client.post(reverse(name, args=[self.record.pk])).status_code, 403
            )
        self.assertEqual(self.client.post(reverse("add_record")).status_code, 403)

    def test_owner_signs_in_with_existing_password(self):
        response = self.client.post(
            reverse("login"), {"username": "owner", "password": "synthetic-test-password"}
        )
        self.assertRedirects(response, reverse("home"))
        self.assertEqual(self.client.get(reverse("admin:index")).status_code, 200)

    def test_owner_can_create_and_update_records(self):
        self.client.force_login(self.owner)
        data = {
            "first_name": "Example", "last_name": "Person", "email": "person@example.com",
            "phone": "01234567890", "address": "1 Test Road", "city": "Test City",
            "postcode": "AB1 2CD",
        }
        self.assertRedirects(self.client.post(reverse("add_record"), data), reverse("home"))
        record = Costumer.objects.get(email="person@example.com")
        data["first_name"] = "Updated"
        detail = reverse("record", args=[record.pk])
        self.assertRedirects(self.client.post(reverse("update_costumer", args=[record.pk]), data), detail)
        self.assertContains(self.client.get(detail), "Updated")

    def test_delete_requires_post_and_csrf(self):
        client = Client(enforce_csrf_checks=True)
        client.force_login(self.owner)
        detail = reverse("record", args=[self.record.pk])
        delete = reverse("delete_costumer", args=[self.record.pk])
        self.assertEqual(client.get(delete).status_code, 405)
        self.assertEqual(client.post(delete).status_code, 403)
        self.assertTrue(Costumer.objects.filter(pk=self.record.pk).exists())
        self.assertEqual(client.get(detail).status_code, 200)
        token = client.cookies["csrftoken"].value
        self.assertRedirects(client.post(delete, HTTP_X_CSRFTOKEN=token), reverse("home"))
        self.assertFalse(Costumer.objects.filter(pk=self.record.pk).exists())
        self.assertEqual(client.get(detail).status_code, 404)
