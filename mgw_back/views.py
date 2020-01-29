from django.http import Http404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from rest_framework.exceptions import ValidationError
import json

from mgw_back.models import MGSession, MGFile
from mgw_back.serializers import MGSessionSerializer, MGSessionDetailSerializer, MGFileSerializer
from mgw_back.tasks import process
from mgw_back.utilities import without_folder


class SessionView(APIView):
    @staticmethod
    def get_session(token):
        try:
            return MGSession.objects.get(token=token)
        except MGSession.DoesNotExist:
            raise Http404

    def get(self, request, token, format=None):
        session = self.get_session(token)
        serializer = MGSessionDetailSerializer(session)
        return Response(serializer.data)


class SessionCreate(APIView):
    def delete_unnecessary_files(self, previous_session, keep_target, keep_reference):
        to_delete = [previous_session.result16, previous_session.result24, previous_session.preview_target,
                     previous_session.preview_result]
        if not keep_target:
            to_delete.append(previous_session.target.file)
        if not keep_reference:
            to_delete.append(previous_session.reference.file)
        for file in to_delete:
            if file:
                file.delete(False)

    def post(self, request, format=None):
        body = json.loads(request.body)

        keep_target = body.get('keep_target', False)
        keep_reference = body.get('keep_reference', False)
        previous_token = body.get('previous')
        if keep_target and keep_reference:
            raise ValidationError

        previous_session = SessionView.get_session(previous_token) if previous_token else None
        session = MGSession.objects.create()

        if previous_session:
            if keep_target:
                session.target = previous_session.target
            if keep_reference:
                session.reference = previous_session.reference
            session.save()
            self.delete_unnecessary_files(previous_session, keep_target, keep_reference)

        serializer = MGSessionSerializer(session)
        return Response(serializer.data)


class UploadFile(APIView):
    parser_classes = (MultiPartParser, )

    def post(self, request, token, file_type, format=None):
        session = SessionView.get_session(token)

        if getattr(session, file_type) or session.code != 2001:
            raise ValidationError

        serializer = MGFileSerializer(data=request.data)
        if serializer.is_valid():
            file = request.FILES['file']
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
