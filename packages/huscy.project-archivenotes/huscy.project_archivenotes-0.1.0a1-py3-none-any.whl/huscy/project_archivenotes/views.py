from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser

from huscy.project_archivenotes import serializer, services


class ArchiveNoteViewSet(viewsets.ModelViewSet):
    queryset = services.get_archive_notes()
    serializer_class = serializer.ArchiveNoteSerializer
    permission_classes = (IsAdminUser, )
