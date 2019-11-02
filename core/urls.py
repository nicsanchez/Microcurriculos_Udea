from django.urls import path
#el punto quiere decir que de este directorio
from . import views 

urlpatterns = [
    path('crear/',views.core,name='core'),
    path('',views.curso,name='curso'),
    path('asignar/',views.asignar,name='asignar'),
    path('nucleo/',views.nucleo,name="nucleo"),
    path('visualizar/',views.visualizar,name="visualizar"),
    path('editar/',views.editar,name="editar"),
    path('crear2/',views.crear2,name="crear2")
]