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
