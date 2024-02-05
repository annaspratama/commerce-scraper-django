from abc import ABC, abstractmethod
from django.http import HttpResponse


class ScrapOlxInterface(ABC):
    """
    Scrap OLX's products data.
    See: https://olx.co.id
    """

    @abstractmethod
    def __init__(self, url: str) -> None:
        """
        Init data.

        Keyword arguments:
        url -- the url site to OLX's products

        Returns:
        None
        """
        pass

    @abstractmethod
    def scrap_olx(self, auto_download: bool = True) -> HttpResponse:
        """
        Scrap OLX's products data.

        Keyword arguments:
        auto_download -- the download feature (default is true)

        Returns:
        HttpResponse -- Excel or CSV file
        """
        pass

    @abstractmethod
    def check_url(self) -> str:
        """
        Check the url
        """
        pass