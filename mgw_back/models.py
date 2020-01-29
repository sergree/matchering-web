from django.db import models

from mgw_back.utilities import random_str_32


class MGFile(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    file = models.FileField()
    title = models.CharField(blank=True, max_length=100)


class MGSession(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    code = models.IntegerField(default=2001)
    token = models.CharField(max_length=32, default=random_str_32, unique=True)

    target = models.ForeignKey(
        MGFile, on_delete=models.CASCADE,
        blank=True, null=True, related_name='%(class)s_target'
    )
    reference = models.ForeignKey(
        MGFile, on_delete=models.CASCADE,
        blank=True, null=True, related_name='%(class)s_reference'
    )

    result16 = models.FileField(blank=True)
    result24 = models.FileField(blank=True)

    preview_target = models.FileField(blank=True)
    preview_result = models.FileField(blank=True)


class MGWarning(models.Model):
    code = models.IntegerField()
    session = models.ForeignKey(MGSession, related_name='warnings', on_delete=models.CASCADE)
