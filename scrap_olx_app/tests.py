from django.test import TestCase
from .services.scrap_service import ScrapOlxService


class ScrapOlxTestCase(TestCase):

    def setUp(self) -> None:
        
        url = "https://olx.co.id"
        self.scrap_service = ScrapOlxService(url=url)
    
    def test_scrap_olx_service(self):
        """Test for scrap olx is working perfectly"""

        test = self.scrap_service.scrap_olx()
        self.assertEqual(first="test", second=test)