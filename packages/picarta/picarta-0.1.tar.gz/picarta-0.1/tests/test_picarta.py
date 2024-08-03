import unittest
from picarta import Picarta

class TestPicarta(unittest.TestCase):
    def setUp(self):
        self.api_token = "YOUR_API_TOKEN"
        self.localizer = Picarta(self.api_token)

    def test_is_valid_url(self):
        self.assertTrue(self.localizer.is_valid_url("https://example.com/image.jpg"))
        self.assertFalse(self.localizer.is_valid_url("not_a_url"))

    def test_localize_image_url(self):
        result = self.localizer.localize("https://upload.wikimedia.org/wikipedia/commons/8/83/San_Gimignano_03.jpg")
        self.assertIsNotNone(result)

    def test_localize_image_local(self):
        result = self.localizer.localize("path/to/local/image.jpg")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
