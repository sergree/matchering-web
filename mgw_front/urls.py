"""
Matchering WEB - Handy Matchering 2.0 Containerized Web Application
Copyright (C) 2016-2020 Sergree

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

from django.urls import path
from django.views.generic import TemplateView, RedirectView

from matchering_web.settings import STATIC_URL

app_name = 'mgw_front'
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('favicon.ico', RedirectView.as_view(url=f'{STATIC_URL}favicon.ico'))
]
