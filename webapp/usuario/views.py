from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from inicio.models import Usuario, CuentaBancaria, Transaccion, ServiciosBancarios
from django.utils import timezone
from random import randint

# Create your views here.


#EDICIÓN DE SERVICIO
#--PETICIÓN POST Y LISTA DE SERVICIOS
def AdministrarServicios(request):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        Cuenta          = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario).last()
        Transacciones   = Transaccion.objects.all().filter(CuentaOrigen=Cuenta)
        template_name   = 'usuario/AdminAdministrarServicios.html'
        return render(request, template_name,{'persona': id_usuario, 'Transacciones': Transacciones})   
    
    else:
        return  HttpResponseRedirect('/inicio')

def AgregarCuentaMostrarTemplate(request):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        template_name   = 'usuario/AdminAgregarCuentas.html'
        return render(request, template_name,{'persona': id_usuario})   
    else:
        return  HttpResponseRedirect('/inicio')

def VerServiciosBancarios(request):
    if request.session.get('usuario'):
        if request.method == 'POST':
            id_servicio       = request.POST.get("Id")
            servicio          = ServiciosBancarios.objects.get(id=id_servicio)
            servicio.NombreServicio                     = request.POST.get("NombreServicio")
            servicio.FechaInicio                        = request.POST.get("FechaInicio")
            servicio.FechaFin                           = request.POST.get("FechaFin")
            servicio.save()
            return  HttpResponseRedirect('/VerServiciosBancarios')
            
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        servicios   = ServiciosBancarios.objects.all().filter()
        if username == 'ggamboac':
            template_name       = 'usuario/AdminVerServicios.html'
            return render(request, template_name, {'persona': id_usuario, 'servicios': servicios})        
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')

def AgregarServicio(request):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        Cuenta          = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario).last()
        Transacciones   = Transaccion.objects.all().filter(CuentaOrigen=Cuenta)
        if request.method == 'POST':
            usuario_admin               = request.POST.get("UsuarioAdmin")
            nombre_servicio_bancario    = request.POST.get("NombreServicioBancario")
            descripcion_servicio_bancario    = request.POST.get("DescripcionServicioBancario")
            ubicacion_servicio          = request.POST.get("UbicacionServicio")
            telefono_servicio           = request.POST.get("TelefonoServicio")
            password                    = request.POST.get("password")
            if usuario_admin is "" or nombre_servicio_bancario is  "" or descripcion_servicio_bancario is  "" or ubicacion_servicio is "" or telefono_servicio is  "" or password is  "":
                return  HttpResponseRedirect('/AdministrarServicios')            
            CrearServicios(usuario_admin, password, nombre_servicio_bancario, descripcion_servicio_bancario, ubicacion_servicio, telefono_servicio)
            return  HttpResponseRedirect('/VerServiciosBancarios')
        else:
            return  HttpResponseRedirect('/AdministrarServicios')

        return  HttpResponseRedirect('/AdministrarServicios')    
    else:
        return  HttpResponseRedirect('/inicio')

#EDICIÓN DE SERVICIO
#--PETICIÓN GET
def EditarServicio(request,id):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        id_servicio       = id
        servicio          = ServiciosBancarios.objects.get(id=id_servicio)
        if username == 'ggamboac':
            template_name       = 'usuario/EditarServicio.html'
            return render(request, template_name, {'persona': id_usuario, 'servicio': servicio})        
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')

#ELIMINACIÓN DE CUENTA 
#--PETICIÓN GET
def EliminarServicio(request,id):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        id_servicio       = id
        servicio          = ServiciosBancarios.objects.get(id=id_servicio)
        if username == 'ggamboac':
            servicio.delete()
            return  HttpResponseRedirect('/VerServiciosBancarios')      
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')


def AgregarCuntasBancarias(request):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        Cuenta          = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario).last()
        Transacciones   = Transaccion.objects.all().filter(CuentaOrigen=Cuenta)
        if request.method == 'POST':
            usuario_admin               = request.POST.get("UsuarioAdmin")
            nombre_servicio_bancario    = request.POST.get("NombreServicioBancario")
            descripcion_servicio_bancario    = request.POST.get("DescripcionServicioBancario")
            ubicacion_servicio          = request.POST.get("UbicacionServicio")
            telefono_servicio           = request.POST.get("TelefonoServicio")
            password                    = request.POST.get("password")
            if usuario_admin is "" or nombre_servicio_bancario is  "" or descripcion_servicio_bancario is  "" or ubicacion_servicio is "" or telefono_servicio is  "" or password is  "":
                return  HttpResponseRedirect('/VerCuentasBancarias')            
            CrearUsuarios(usuario_admin, password, nombre_servicio_bancario, descripcion_servicio_bancario, ubicacion_servicio, telefono_servicio)
            return  HttpResponseRedirect('/VerCuentasBancarias')
        else:
            return  HttpResponseRedirect('/VerCuentasBancarias')

        return  HttpResponseRedirect('/VerCuentasBancarias')    
    else:
        return  HttpResponseRedirect('/inicio')

def VerUsuarios(request):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        usuarios   = Usuario.objects.all().filter()
        if username == 'ggamboac':
            template_name       = 'usuario/AdminVerUsuarios.html'
            return render(request, template_name, {'persona': id_usuario, 'usuarios': usuarios})        
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')

#ELIMINACIÓN DE USUARIO 
#--PETICIÓN GET
def EliminarUsuario(request,id):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        usuario      = Usuario.objects.get(id=id)
        if username == 'ggamboac':
            usuario.delete()
            return  HttpResponseRedirect('/AdminVerUsuarios')      
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')

#PETICIÓN POST DE LA EDICIÓN DE LA CUENTA 
#RENDER DE LA LISTA DE CUENTAS BANCARIAS
def VerCuentasBancarias(request):
    if request.session.get('usuario'):
        if request.method == 'POST':
            id_cuenta = request.POST.get("numero_cuenta")
            cuenta = CuentaBancaria.objects.get(NumeroCuentaBancaria=id_cuenta)
            cuenta.saldo           = request.POST.get("saldo")
            cuenta.FechaInicio     = request.POST.get("fecha_inicio")
            cuenta.FechaFin        = request.POST.get("fecha_fin")
            cuenta.save()
            return  HttpResponseRedirect('/VerCuentasBancarias')

        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        cuentas   = CuentaBancaria.objects.all().filter()
        if username == 'ggamboac':
            template_name       = 'usuario/AdminVerCuentas.html'
            return render(request, template_name, {'persona': id_usuario, 'cuentas': cuentas})        
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')

#EDICIÓN DE CUENTA
#--PETICIÓN GET
def EditarCuenta(request,id):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        id_cuenta       = id
        cuenta          = CuentaBancaria.objects.get(NumeroCuentaBancaria=id_cuenta)
        if username == 'ggamboac':
            template_name       = 'usuario/EditarCuenta.html'
            return render(request, template_name, {'persona': id_usuario, 'cuenta': cuenta})        
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')

#ELIMINACIÓN DE CUENTA 
#--PETICIÓN GET
def EliminarCuenta(request,id):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        id_cuenta       = id
        cuenta          = CuentaBancaria.objects.get(NumeroCuentaBancaria=id_cuenta)
        if username == 'ggamboac':
            cuenta.delete()
            return  HttpResponseRedirect('/VerCuentasBancarias')      
        return  HttpResponseRedirect('/inicio')
    else:
        return  HttpResponseRedirect('/inicio')



def CrearServicios(usuario, password, nombre, apellido, direccion, telefono):    
    srv1 = ServiciosBancarios()
    srv1.id = randint(1000000, 9000000)
    srv1.NumeroCuentaBancaria = CrearUsuarios(usuario, password, nombre, apellido, direccion, telefono)
    srv1.NombreServicio = apellido
    srv1.FechaInicio = timezone.now() 
    srv1.save()

def CrearUsuarios( usuario, password, nombre, apellido, direccion, telefono):
    usr8            = Usuario()
    usr8.id         = randint(1000000, 9000000)  
    usr8.usuario    = usuario
    usr8.password   = password
    usr8.Nombre     = nombre
    usr8.Apellido   = apellido
    usr8.direccion  = direccion
    usr8.telefono   = telefono
    usr8.Fecha_Creacion = timezone.now()    
    usr8.save()

    ct1 = CuentaBancaria()
    ct1.NumeroCuentaBancaria = randint(1000000, 9000000) 
    ct1.UsuarioPropietario = usr8
    ct1.saldo = 0
    ct1.FechaInicio = timezone.now()
    ct1.save()

    return ct1