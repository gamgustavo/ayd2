from django.conf.urls import url
from inicio.views import carga_datos
from inicio.views import inicio
from transacciones.views import inicio_transacciones,RealizarTransacciones,HistorialTransacciones,VerHistorialCuenta,PracticaAnalisis
from usuario.views import EliminarUsuario,EliminarServicio,EditarServicio,EliminarCuenta,EditarCuenta,VerUsuarios,AdministrarServicios, AgregarServicio, VerServiciosBancarios, AgregarCuntasBancarias,VerCuentasBancarias,AgregarCuentaMostrarTemplate
#from transacciones import views



urlpatterns = [    
    #URL Login
    url('carga_datos/$', carga_datos),
    url('inicio/$', inicio),
    url('transacciones/$', inicio_transacciones),
    url('RealizarTransaccion/$', RealizarTransacciones),
    url('HistorialTransacciones/$', HistorialTransacciones),
    url('VerHistorialCuenta/$', VerHistorialCuenta),
    url('PracticaAnalisis/$', PracticaAnalisis),
    url('AdministrarServicios/$', AdministrarServicios ),    
    url('AgregarServicio/$', AgregarServicio),
    url('VerServiciosBancarios/$', VerServiciosBancarios),
    url('AgregarCuntasBancarias/$', AgregarCuntasBancarias),
    url('VerCuentasBancarias/$', VerCuentasBancarias),
    url('VerUsuarios/$', VerUsuarios),
    url('AgregarCuentaMostrarTemplate/$', AgregarCuentaMostrarTemplate),
    url('EditarCuenta/(?P<id>\d+)$', EditarCuenta),
    url('EliminarCuenta/(?P<id>\d+)$', EliminarCuenta),
    url('EditarServicio/(?P<id>\d+)$', EditarServicio),
    url('EliminarServicio/(?P<id>\d+)$', EliminarServicio),
    url('EliminarUsuario/(?P<id>\d+)$', EliminarUsuario),

]
