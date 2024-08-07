import pytest
from model_bakery import baker

from rest_framework.test import APIClient

#from huscy.project_archivenotes.models import ArchiveNote


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username='user', password='password',
                                                 first_name='Anne', last_name='Theke')


@pytest.fixture
def admin_client(admin_user):
    client = APIClient()
    client.login(username=admin_user.username, password='password')
    return client


@pytest.fixture
def client(user):
    client = APIClient()
    client.login(username=user.username, password='password')
    return client


@pytest.fixture
def anonymous_client():
    return APIClient()


@pytest.fixture
def project():
    return baker.make('projects.Project')


@pytest.fixture
def archive_note(project):
    return None
    return baker.make(
        'project_archivenotes.ArchiveNote',
        action=ArchiveNote.ACTIONS.get_value('store'),
        note='2 folders, filling cabinet A12. compartment 1',
        project=project
    )
