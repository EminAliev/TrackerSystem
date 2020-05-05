from django.contrib import admin

# Register your models here.
from tasks.models import Task, User, Project, Definition

admin.site.register(Task)
#admin.site.unregister(User)
admin.site.register(Project)
admin.site.register(Definition)
