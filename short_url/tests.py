import uuid
from unittest.mock import patch

from rest_framework.test import APITestCase

from short_url.models import ShortUrl


class ShortURLTestCase(APITestCase):
    def setUp(self) -> None:
        self.url = '/'
        self.not_unique_alias = str(uuid.uuid4())[:6]
        ShortUrl.objects.create(
            url="google.com",
            alias=self.not_unique_alias
        )

    def test_create_short_url(self):
        #   Prepare
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        alias = str(uuid.uuid4())[:6]

        #   Act
        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.return_value = alias
            response = self.client.post(self.url, {"url": url})

        #   Assert
        self.assertIn(alias, response.data["short_url"])

    def test_create_short_url_generated_duplicate_alias(self):
        #   Prepare

        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        alias = str(uuid.uuid4())[:6]

        #   Act

        with patch("uuid.uuid4") as mock_uuid:
            mock_uuid.side_effect = [self.not_unique_alias, alias]
            response = self.client.post(self.url, {"url": url})

        #   Assert
        self.assertIn(alias, response.data["short_url"])

    def test_get_full_url(self):
        #   Prepare

        alias = self.not_unique_alias

        #   Act

        response = self.client.get(f"{self.url}{alias}/url/")

        #   Assert
        self.assertEqual("google.com", response.data["url"])

    def test_get_full_url_and_redirect(self):
        # Prepare
        alias = self.not_unique_alias
        url = "google.com"
        #   Act
        response = self.client.get(f"{self.url}{alias}", follow=True)
        #   Assert
        self.assertIn(url, response.redirect_chain[1])
