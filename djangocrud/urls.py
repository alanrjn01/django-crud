
from django.contrib import admin
from django.urls import path,include

'''
definiendo las rutas de la aplicacion:
con include importo las rutas de urls.py de mi aplicacion "tasks"
'''
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('tasks.urls'))
]
