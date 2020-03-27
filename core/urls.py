from django.urls import path
#el punto quiere decir que de este directorio
from . import views 
from django.conf import settings


urlpatterns = [
    path('crear/',views.core,name='core'),
    path('',views.curso,name='curso'),
    path('asignar/',views.asignar,name='asignar'),
    path('nucleo/',views.nucleo,name="nucleo"),
    path('visualizar/',views.visualizar,name="visualizar"),
    path('editar/',views.editar,name="editar"),
    path('crear2/',views.crear2,name="crear2"),
    path('nuevo1/',views.nuevo1,name="nuevo1"),
    path('nuevo2/',views.nuevo2,name="nuevo2"),
    path('nuevo3/',views.nuevo3,name="nuevo3"),
    path('nuevo4/',views.nuevo4,name="nuevo4"),
    path('logout/',views.logout,name="logout"),
    path('login/',views.login,name="login"),
    path('peticiones/',views.peticiones,name="peticiones")
]
if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)