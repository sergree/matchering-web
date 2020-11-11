"""
Matchering WEB - Handy Matchering 2.0 Containerized Web Application
Copyright (C) 2016-2021 Sergree

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

from django.http import Http404
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError
import json
from datetime import timedelta

from matchering_web.settings import MGW_STORE_DATA_FOR_MINUTES
from mgw_back.models import MGSession, MGFile
from mgw_back.serializers import (
    MGSessionSerializer,
    MGSessionDetailSerializer,
    MGFileSerializer,
)
from mgw_back.tasks import process
from mgw_back.utilities import without_folder


class SessionView(APIView):
    @staticmethod
    def get_session(token, raise404=True):
        try:
            return MGSession.objects.get(token=token)
        except MGSession.DoesNotExist:
            if raise404:
                raise Http404

    def get(self, request, token, format=None):
        session = self.get_session(token)
        serializer = MGSessionDetailSerializer(session)
        return Response(serializer.data)


class SessionCreate(APIView):
    def remove_previous(self, previous_session, keep_target, keep_reference):
        if not keep_target:
            previous_session.target.delete()
        if not keep_reference:
            previous_session.reference.delete()
        previous_session.delete()

    def remove_old(self):
        time_threshold = timezone.now() - timedelta(minutes=MGW_STORE_DATA_FOR_MINUTES)
        MGSession.objects.filter(updated__lte=time_threshold).delete()
        MGFile.objects.filter(used__lte=time_threshold).delete()

    def post(self, request, format=None):
        body = json.loads(request.body)

        keep_target = body.get("keep_target", False)
        keep_reference = body.get("keep_reference", False)
        previous_token = body.get("previous")
        if keep_target and keep_reference:
            raise ValidationError

        previous_session = (
            SessionView.get_session(previous_token, raise404=False)
            if previous_token
            else None
        )
        session = MGSession.objects.create()

        if previous_session:
            if keep_target:
                session.target = previous_session.target
                session.target.save()
            if keep_reference:
                session.reference = previous_session.reference
                session.reference.save()
            session.save()
            self.remove_previous(previous_session, keep_target, keep_reference)

        self.remove_old()

        serializer = MGSessionSerializer(session)
        return Response(serializer.data)


class UploadFile(APIView):
    parser_classes = (MultiPartParser,)

    def post(self, request, token, file_type, format=None):
        session = SessionView.get_session(token)

        if getattr(session, file_type) or session.code != 2001:
            raise ValidationError

        serializer = MGFileSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES["file"]
            instance = MGFile.objects.create(file=file, title=without_folder(file.name))
            setattr(session, file_type, instance)

            if session.target and session.reference:
                session.code = 2002
                session.save()
                process.delay(session)
            else:
                session.save()

            return Response(status=status.HTTP_201_CREATED)
        else:
            raise ValidationError
