from typing import Any
from django.http import HttpRequest, HttpResponse
from django.views.generic.base import View, TemplateView
from .services.scrap_service import ScrapOlxService


class ScrapOlxProductsDisplay(TemplateView):

    template_name = "home.html"
    

class ScrapProducts(TemplateView):
    
    template_name = "home.html"

    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        """
        Scarp OLX's products.

        Keyword arguments:
            - request -- HttpRequest

        Returns:
            - none
        """

        url = request.POST.get('url')
        self.service = ScrapOlxService(url=url)

        return super().setup(request, *args, **kwargs)

    def post(self, request: HttpRequest) -> HttpResponse:
        """
        Scrap OLX data by given URL.
        Then download it as excel file.

        Keyword arguments:
            - request -- HttpRequest

        Returns:
            - HttpResponse -- download as excel file
        """

        print('method: ', request.method)
        if request.method == 'POST' and request.POST.get('commerce') == "olx": return self.service.scrap_olx()
        else: HttpResponse(content="Method not allowed.", status=401)