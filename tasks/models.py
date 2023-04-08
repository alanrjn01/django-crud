from django.db import models
from django.contrib.auth.models import User

'''
creando un modelo para las tareas con distintos atributos
1. el atributo user se relaciona con la tabla de usuarios
2. datecompleted sirve para establecer una fecha de tarea completada para conocer si la tarea
se realizo o no.
3. important es un atributo booleano que por defecto se marca en false
4. created se autoagrega la fecha actual
blank=True sirve para especificar que el input del form puede estar vacio
'''
class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=300,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    datecompleted = models.DateTimeField(null=True,blank=True)
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    '''
    cuando se utiliza el modelo Task como string va a retornar su titulo
    '''
    def __str__(self):
        return self.title