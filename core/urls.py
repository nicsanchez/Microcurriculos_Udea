from django.urls import path
#el punto quiere decir que de este directorio
from . import views 

urlpatterns = [
    path('crear/',views.core,name='core'),
    path('',views.curso,name='curso'),
    path('asignar/',views.asignar,name='asignar')
]