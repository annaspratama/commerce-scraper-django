from django.http import HttpResponse
from scrap_olx_app.interfaces.scrap_interface import ScrapOlxInterface


class ScrapOlxService(ScrapOlxInterface):
    
    def __init__(self, url: str) -> None:
        self.url = url

    def scrap_olx(self, auto_download: bool = True) -> HttpResponse:
        return "test"
    
    def check_url(self) -> str:
        return "ok"