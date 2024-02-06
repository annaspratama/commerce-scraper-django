from django.urls import path
from scrap_olx_app.views import ScrapProducts

app_name = 'scrap_olx_app'

urlpatterns = [
    path(route='', view=ScrapProducts.as_view(), name='scrap-products')
]