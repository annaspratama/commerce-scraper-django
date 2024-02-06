from abc import ABC, abstractmethod
from django.http import HttpResponse


class ScrapOlxInterface(ABC):
    """
    Scrap OLX's products data.
    See: https://www.olx.co.id
    """

    @abstractmethod
    def __init__(self, url: str = None) -> None:
        """
        Init data.

        Keyword arguments:
        url -- the url site to OLX's products

        Returns:
        None
        """
        pass

    @abstractmethod
    def scrap_olx(self, auto_download: bool = True) -> HttpResponse|Exception:
        """
        Scrap OLX's products data.

        Keyword arguments:
        auto_download -- the download feature (default is true)

        Returns:
        HttpResponse -- Excel or CSV file if success
        Exception -- Raise an exception if fail
        """
        pass

    @abstractmethod
    def validate_url(self) -> bool:
        """
        Check the url
        """
        pass