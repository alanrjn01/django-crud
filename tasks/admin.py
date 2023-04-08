from django.contrib import admin
from .models import Task

#registrando en el panel de administracion el modelo de Tareas
admin.site.register(Task)
