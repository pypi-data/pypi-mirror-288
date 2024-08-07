#from enum import Enum

#from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

#from huscy.projects.models import Project


"""
class ArchiveNote(models.Model):
    class ACTIONS(Enum):
        store = (0, 'store')
        retrieve = (1, 'retrieve')
        other = (255, 'other')

        @classmethod
        def get_value(cls, member):
            return cls[member].value[0]

    note = models.TextField(max_length=1024)
    action = models.PositiveSmallIntegerField(choices=[(x.value) for x in ACTIONS])
    created_at = models.DateTimeField(auto_now_add=True)
    depositor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    depositor_name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
"""


class User(AbstractUser):
    display_name = models.CharField(max_length=128)

    class Meta:
        db_table = 'auth_user'
