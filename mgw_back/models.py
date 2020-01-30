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

from django.db import models

from mgw_back.utilities import random_str_32


class MGFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    used = models.DateField(auto_now=True)
    file = models.FileField()
    title = models.CharField(blank=True, max_length=100)


class MGSession(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.IntegerField(default=2001)
    token = models.CharField(max_length=32, default=random_str_32, unique=True)

    target = models.ForeignKey(
        MGFile, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='%(class)s_target'
    )
    reference = models.ForeignKey(
        MGFile, on_delete=models.SET_NULL,
        blank=True, null=True, related_name='%(class)s_reference'
    )

    result16 = models.FileField(blank=True)
    result24 = models.FileField(blank=True)

    preview_target = models.FileField(blank=True)
    preview_result = models.FileField(blank=True)


class MGWarning(models.Model):
    code = models.IntegerField()
    session = models.ForeignKey(MGSession, related_name='warnings', on_delete=models.CASCADE)
