from rest_framework import serializers

from huscy.project_archivenotes import models


class ArchiveNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ArchiveNote
        fields = (
            'action',
            'created_at',
            'depositor',
            'depositor_name',
            'id',
            'note',
            'project',
        )
        read_only_fields = (
            'created_at',
        )
