from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from pymongo import MongoClient
from .models import Cuenta
import datetime
from django.http import HttpResponseRedirect
from .models import Cuenta,Usuario,CuentaBancaria,ServiciosBancarios,Transaccion
from django.utils import timezone
from random import randint
from django.template import RequestContext

from decimal import Decimal


import cProfile, pstats, sys

# Create your views here.

#Codigo destinado a la carga de datos iniciales de la aplicación.
def carga_datos(request):

    Cuenta.objects.all().delete()
    Usuario.objects.all().delete()    
    CuentaBancaria.objects.all().delete()
    ServiciosBancarios.objects.all().delete()
    Transaccion.objects.all().delete()    
    


    CrearUsuarios('ggamboac','admin','Gustavo Adolfo','Gamboa Cruz','USAC',59377035)
    ##CrearUsuarios('jarango','admin','Julio Alberto','Arango Godinez','USAC',59377035)
    ##CrearUsuarios('jsierra','admin','Julia Argentina','Sierra Herrera','USAC',59377035)   
    CrearUsuarios('achinchilla','admin','Alba Janeth','Chinchilla','USAC',59377035)
    CrearUsuarios('dgarcia','admin','Daniel','Garcia','USAC',59377035)
    CrearUsuariosPruebas()
 




    n = Cuenta()
    n.id = 1
    n.usuario = 'gamgustavo'
    n.password = 'password'
    n.saldo = 512
    n.save()

    n2 = Cuenta()
    n2.id = 2
    n2.usuario = 'danielgarcia'
    n2.password = 'password'
    n2.saldo = 850
    n2.save()    


    DatosCargados = CuentaBancaria.objects.count()
    return  HttpResponse("Carga de Datos: " + str(DatosCargados))  


#LOGIN.
#--
#Vista de login de la aplicación.
@csrf_exempt
def inicio(request):
    if request.session.get('usuario'):
        del request.session['usuario']
    template_name = 'inicio/page-login.html'
    return render(request, template_name)

#Vista de validación de login de la aplicación.
@csrf_exempt
def inicio_sesion(request):  
    pr = cProfile.Profile()
    pr.enable()   
    if request.session.get('usuario') and request.session.get('password'):
        email       = request.session['usuario']
        password    = request.session['password']
        Logueado    = Usuario.objects.get(usuario=email,password=password)
        id_usuario  = Usuario.objects.get(usuario=email,password=password)
        request.session['usuario'] = email
        request.session['password'] = password
        CuentasBancarias    = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario)       
        #validacion si es usuario administrador
        if email == 'ggamboac':
            ps = pstats.Stats(pr, stream=sys.stdout)
            #ps.print_stats()
            pr.disable()
            pr.dump_stats('profile1.prof')
            return  HttpResponseRedirect('/VerServiciosBancarios')       
        template_name       = 'usuario/home.html'
        ps = pstats.Stats(pr, stream=sys.stdout)
        #ps.print_stats()
        pr.disable()
        pr.dump_stats('profile1.prof')
        return render(request, template_name,{'persona': Logueado, 'Cuentas': CuentasBancarias})        

    if request.method == 'POST':
        email       = request.POST.get("email")
        password    = request.POST.get("password")
        if email is "" or password is  "":
            ps = pstats.Stats(pr, stream=sys.stdout)
            #ps.print_stats()
            pr.disable()
            pr.dump_stats('profile1.prof')
            return HttpResponseRedirect('/inicio')
        existe = Usuario.objects.filter(usuario=email,password=password).exists()
        if existe == True:
            Logueado        = Usuario.objects.get(usuario=email,password=password)
            id_usuario      = Usuario.objects.get(usuario=email,password=password)
            request.session['usuario']  = email
            request.session['password'] = password
            CuentasBancarias    = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario)            
            #Validacion usuario administrador
            if email == 'ggamboac':
                ps = pstats.Stats(pr, stream=sys.stdout)
               # ps.print_stats()
                pr.disable()
                pr.dump_stats('profile1.prof')
                return  HttpResponseRedirect('/VerServiciosBancarios')
            template_name       = 'usuario/home.html'
            ps = pstats.Stats(pr, stream=sys.stdout)
            #ps.print_stats()
            pr.disable()
            pr.dump_stats('profile1.prof')
            return render(request, template_name,{'persona': Logueado, 'Cuentas': CuentasBancarias})
        else:
            ps = pstats.Stats(pr, stream=sys.stdout)
            #ps.print_stats()
            pr.disable()
            pr.dump_stats('profile1.prof')
            return HttpResponseRedirect('/inicio')
    else:
        ps = pstats.Stats(pr, stream=sys.stdout)
        #ps.print_stats()
        pr.disable()
        pr.dump_stats('profile1.prof')
        return HttpResponseRedirect('/inicio')
    

def CrearUsuarios( usuario, password, nombre, apellido, direccion,telefono):
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
    ct1.saldo = 50
    ct1.FechaInicio = timezone.now()
    ct1.save()

    ct2 = CuentaBancaria()
    ct2.NumeroCuentaBancaria = randint(1000000, 9000000) 
    ct2.UsuarioPropietario = usr8
    ct2.saldo = 835
    ct2.FechaInicio = timezone.now()
    ct2.save()    

    return ct1

def CrearServicios():    
    srv1 = ServiciosBancarios()
    srv1.id = randint(1000000, 9000000)
    srv1.NumeroCuentaBancaria = CrearUsuarios('calusac','admin','Calusac','Centro Estudios','USAC',59377035)
    srv1.NombreServicio = 'Centro Estudio Lenguas'
    srv1.FechaInicio = timezone.now()
    srv1.save()


def CrearTransaccion(CuentaOrigen, CuentaDestino,DebitoCredito,Monto,Descripcion):

    existeOrigen = CuentaBancaria.objects.filter(NumeroCuentaBancaria=CuentaOrigen).exists()
    existeDestino = CuentaBancaria.objects.filter(NumeroCuentaBancaria=CuentaDestino).exists()

    if existeOrigen == True and existeDestino == True:
        trx = Transaccion()
        trx.id = randint(1000000, 9000000) 
        trx.CuentaOrigen = CuentaBancaria.objects.get(NumeroCuentaBancaria=CuentaOrigen)
        trx.CuentaDestino = CuentaBancaria.objects.get(NumeroCuentaBancaria=CuentaDestino)
        trx.Monto = Monto
        trx.FechaTransaccion = timezone.now()
        trx.DescripcionTransaccion = Descripcion
        trx.save()


def CrearUsuariosPruebas():
    usr8            = Usuario()
    usr8.id         = randint(1000000, 9000000)  
    usr8.usuario    = 'jarango'
    usr8.password   = 'admin'
    usr8.Nombre     = 'Julio Alberto'
    usr8.Apellido   = 'Arango Gondinez'
    usr8.direccion  = 'USAC'
    usr8.telefono   = 4626562
    usr8.Fecha_Creacion = timezone.now()    
    usr8.save()

    ct1 = CuentaBancaria()
    ct1.NumeroCuentaBancaria = 2622071 
    ct1.UsuarioPropietario = usr8
    ct1.saldo = Decimal(5000)
    ct1.FechaInicio = timezone.now()
    ct1.save()

    ct2 = CuentaBancaria()
    ct2.NumeroCuentaBancaria = 4529844
    ct2.UsuarioPropietario = usr8
    ct2.saldo = 5000
    ct2.FechaInicio = timezone.now()
    ct2.save() 

    usr9            = Usuario()
    usr9.id         = randint(1000000, 9000000)  
    usr9.usuario    = 'jsierra'
    usr9.password   = 'admin'
    usr9.Nombre     = 'Julia Argentina'
    usr9.Apellido   = 'Sierra Herrera'
    usr9.direccion  = 'USAC'
    usr9.telefono   = 4626562
    usr9.Fecha_Creacion = timezone.now()    
    usr9.save()

    ct3 = CuentaBancaria()
    ct3.NumeroCuentaBancaria = 2234792 
    ct3.UsuarioPropietario = usr9
    ct3.saldo = 5000
    ct3.FechaInicio = timezone.now()
    ct3.save()

    ct4 = CuentaBancaria()
    ct4.NumeroCuentaBancaria = 5941858
    ct4.UsuarioPropietario = usr9
    ct4.saldo = 5
    ct4.FechaInicio = timezone.now()
    ct4.save() 




#--

