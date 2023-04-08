from django.shortcuts import render,redirect,get_object_or_404
#UserCreationForm -> formulario para crear un usuario
#AuthenticationForm -> Para comprobar si el usuario ya existe
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from .forms import CreateTaskForm
from .models import Task
from django.utils import timezone

#request es un parametro que django ofrece para obtener información del cliente
def home(request):
    return render(request,'home.html')

'''
cada vez que se envia un formulario se vuelve a llamar a la misma url por lo cual:

1- si el request llega a traves de get se renderiza signup.html con el formulario de UserCreationForm
||
2- si el request llega con informacion en el post y las contrasenias ingresadas son iguales
    se realiza un registro en la base de datos con los datos obtenidos del request.POST
    al ser una consulta en la base de datos, utilizo un try y except para determinar si la consulta
    fue exitosa o no
'''
def signup(request):
    #si es get renderizo el formulario
    if request.method == 'GET':
        print("mostrando formulario")
        return render(request,'signup.html',{
        'form':UserCreationForm
        })
    else:
        if request.method =='POST' and request.POST['password1'] == request.POST['password2']:
            #try -> intenta realizar la insercion en la base de datos 
            try:
                #registrando usuario en la base de datos:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1']
                )
                user.save()
                # login -> guardando en una cookie el usuario creado
                login(request,user)
                return redirect('tasks')
            except IntegrityError:
                #en caso de que la consulta en la base de datos tire una excepcion 
                #renderizo signup.html con 'notif' de usuario ya existente
                #en este caso, en el except manejo IntegrityError
                return render(request,'signup.html',{
                    'form':UserCreationForm,
                    'notif':'¡el usuario ya existe!'
                })
        else:
            #en caso de que las contrasenias no coincidan se informa en 'notif'
            return render(request,'signup.html',{
                'form':UserCreationForm,
                'notif':'¡las contrasenias no coinciden!'
            })
        
'''
    obtengo el id del usuario de la sesion activa
    filtro en la tabla de task por tareas con el id de la sesion actual
    busco tanto las tareas realizadas como las no realizadas. esto a traves de datecompleted__isnull
    -> compruebo si la fecha de completado es true o false para saber si las tareas estan hechas o no
'''
@login_required
def tasks(request):
    current_user = request.user.id
    pending_tasks_from_db = Task.objects.filter(user_id=current_user,datecompleted__isnull=True)
    finished_tasks_from_db = Task.objects.filter(user_id=current_user,datecompleted__isnull=False)
    return render(request,'tasks.html',{
        'pending_tasks_from_db':pending_tasks_from_db,
        'finished_tasks_from_db':finished_tasks_from_db
    })

@login_required
def logout_from_app(request):
    logout(request)
    return redirect('home')


def login_app(request):
    if request.method == 'GET':
        return render(request,'login.html',{
            'form':AuthenticationForm
        })
    else:
        #con authenticate corroboro si los datos ingresadas son correctas
        #si el user es vacio es porque no se pudo logear, de lo contrario el logeo es exitoso
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'login.html',{
                'form':AuthenticationForm,
                'notif':'Usuario o contrasenia incorrecto'
            })
        else:
            #importante usar el login para guardar la sesion
            login(request,user)
            return redirect('tasks')
       
'''
para crear la tarea utilizo el request.POST para comprobar si fue marcada la opcion booleana 'important'
por defecto no se marca entonces inicializo la variable en 0, si en el request se recibe un 'important'
es porque se marco como importante, entonces lo paso a 1
Posteriormente creo el objeto con los datos y el usuario asociado con el que esta iniciada la sesion
y despues guardo la tarea en la base de datos y redirecciono a la pagina de tareas
''' 
@login_required
def create_task(request):
    print(request.method)
    if request.method == 'GET':
        return render(request,'create_task.html',{
            'form':CreateTaskForm
        })
    else:
        important = 0
        try:
            
            if request.POST.get('important'):
                important = 1
                
            task = Task.objects.create(
                title=request.POST['title'],
                description=request.POST['description'],
                important=important,
                user_id=request.user.id
            )
            task.save()
            return redirect('tasks')
        
        except ValueError:
            return render(request,'tasks.html',{
                'error':True
            })
          
'''
uso get_object_or_404 para buscar si en la tabla tareas hay una coincidencia con la primary key
y la id ingresada en la url como parametro y asi mostrar esa tarea en el html
    1.a su vez puedo editar la tarea.
    -> la tarea la edito generando un formulario a partir de mi modelo de formulario para la tarea
    -> pero a este le agrego una instancia de la tarea obtenida de la base de datos

'''  
@login_required
def task_detail(request,id):
    user_id=current_user = request.user.id
    if request.method == 'GET':
        task = get_object_or_404(Task,pk=id,user_id=current_user)
        update_form = CreateTaskForm(instance=task)
        return render(request,'task_detail.html',{
            'task':task,
            'update_form':update_form
        })
    else:
        task = get_object_or_404(Task,pk=id,user_id=current_user)
        #creo un nuevo taskform con los datos del request.post y uso como instancia la tarea encontrada
        #guardo ese formulario en la base de datos y asi actualizo el registro
        form = CreateTaskForm(request.POST,instance=task)
        form.save()
        return redirect('tasks')
        
@login_required
def complete_task(request,id):
    task = get_object_or_404(Task,pk=id,user_id=request.user.id)
    if request.method == 'POST':
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required    
def delete_task(request,id):
    task = get_object_or_404(Task,pk=id,user_id=request.user.id)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')
    