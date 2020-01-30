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

from rest_framework import serializers

from mgw_back.models import MGSession, MGFile


class MGSessionSerializer(serializers.ModelSerializer):
    target = serializers.SlugRelatedField(slug_field='title', read_only=True)
    reference = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = MGSession
        fields = ['token', 'target', 'reference']


class MGSessionDetailSerializer(serializers.ModelSerializer):
    warnings = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='code'
    )
    target = serializers.SlugRelatedField(slug_field='title', read_only=True)
    reference = serializers.SlugRelatedField(slug_field='title', read_only=True)

    class Meta:
        model = MGSession
        fields = ['created', 'code', 'target', 'reference', 'result16',
                  'result24', 'preview_target', 'preview_result', 'warnings']


class MGFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = MGFile
        fields = ['file']
