from huscy.project_archivenotes.models import ArchiveNote


def get_archive_notes(project=None):
    qs = ArchiveNote.objects.order_by('project__id', 'created_at')
    if project:
        qs = qs.filter(project=project)
    return qs
