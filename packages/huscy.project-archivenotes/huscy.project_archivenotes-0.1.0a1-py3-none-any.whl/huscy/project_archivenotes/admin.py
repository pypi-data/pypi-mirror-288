from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from huscy.project_archivenotes.models import User


admin.site.register(User, UserAdmin)
