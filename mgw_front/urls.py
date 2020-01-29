from django.urls import path
from django.views.generic import TemplateView, RedirectView

from matchering_web.settings import STATIC_URL

app_name = 'mgw_front'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('favicon.ico', RedirectView.as_view(url=f'{STATIC_URL}favicon.ico'))
]
