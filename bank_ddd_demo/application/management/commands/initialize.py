from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from api.models import Project

new_group, created = Group.objects.get_or_create(name='allowed-traders')
ct = ContentType.objects.get_for_model(Project)

# Now what - Say I want to add 'Can add project' permission to new_group?
permission = Permission.objects.create(codename='can_add_project',
                                   name='Can add project',
                                   content_type=ct)
new_group.permissions.add(permission)
