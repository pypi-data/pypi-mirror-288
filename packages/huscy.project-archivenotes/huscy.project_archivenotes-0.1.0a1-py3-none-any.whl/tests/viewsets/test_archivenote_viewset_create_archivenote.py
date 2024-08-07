from rest_framework.reverse import reverse
from rest_framework.status import HTTP_201_CREATED, HTTP_403_FORBIDDEN

from huscy.project_archivenotes.models import ArchiveNote


def test_admin_user_can_create_archive_note(admin_client, user, project):
    response = create_archive_note(admin_client, user, project)

    assert response.status_code == HTTP_201_CREATED


def test_user_cannot_create_archive_note(client, user, project):
    response = create_archive_note(client, user, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def test_anonymous_user_cannot_create_archive_note(anonymous_client, user, project):
    response = create_archive_note(anonymous_client, user, project)

    assert response.status_code == HTTP_403_FORBIDDEN


def create_archive_note(client, user, project):
    data = dict(
        action=ArchiveNote.ACTIONS.get_value('store'),
        note='note',
        depositor=user.id,
        depositor_name=user.username,
        project=project.id,
    )
    return client.post(reverse('archivenote-list'), data=data)
