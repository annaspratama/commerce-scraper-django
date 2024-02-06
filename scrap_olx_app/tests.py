from django.test import TestCase
from .services.scrap_service import ScrapOlxService


class ScrapOlxTestCase(TestCase):

    def test_valid_url(self):
        """Test for validation the url"""

        scrap_service = ScrapOlxService(url="https://www.olx.co.id")
        is_valid = scrap_service.validate_url()
        self.assertEqual(first=True, second=is_valid)

    def test_not_valid_url(self):
        """Test for validation the url"""

        scrap_service = ScrapOlxService(url="https://google.com")
        is_valid = scrap_service.validate_url()
        self.assertEqual(first=False, second=is_valid)
    
    def test_scrap_olx_service_success(self):
        """Test for scrap olx is success"""

        scrap_service = ScrapOlxService(url="https://www.olx.co.id/jebres_g5001914/q-iphone")
        result = scrap_service.scrap_olx(auto_download=True)
        self.assertEqual(first="Success", second=result)

    def test_scrap_olx_service_fail(self):
        """Test for scrap olx is fail"""

        scrap_service = ScrapOlxService()
        with self.assertRaises(expected_exception=Exception): scrap_service.scrap_olx()