from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Priority)
admin.site.register(models.Status)
admin.site.register(models.Task)