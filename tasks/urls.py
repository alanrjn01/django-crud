from django.urls import path
from .views import home,signup,tasks,logout_from_app,login_app,create_task,task_detail,complete_task,delete_task

'''
creando urls para nuestra aplicacion

'''
urlpatterns=[
    path('',home,name='home'),
    path('signup/',signup,name='signup'),
    path('tasks/',tasks,name='tasks'),
    path('logout/',logout_from_app,name='logout'),
    path('login/',login_app,name='login'),
    path('tasks/create',create_task,name='create_task'),
    path('tasks/<int:id>',task_detail,name='task_detail'),
    path('tasks/<int:id>/complete',complete_task,name='complete_task'),
    path('tasks/<int:id>/delete',delete_task,name='delete_task')
]