from django.shortcuts import render
from django.views.generic import TemplateView
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from inicio.models import Usuario, CuentaBancaria,Transaccion
from django.views.decorators.csrf import csrf_exempt
import json
from django.utils import timezone
from random import randint
import cProfile, pstats, sys
# Create your views here.

@csrf_exempt
def inicio_transacciones(request):
    if request.session.get('usuario'):
        email       = request.session['usuario']
        Logueado    = Usuario.objects.get(usuario=email)
        id_usuario  = Usuario.objects.get(usuario=email)
        CuentasBancarias    = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario)            
        template_name       = 'transacciones/home.html'
        return render(request, template_name,{'persona': Logueado, 'Cuentas': CuentasBancarias})   
    else:
        return  HttpResponseRedirect('/inicio')     

@csrf_exempt
def RealizarTransacciones(request):
    pr = cProfile.Profile()
    pr.enable()
    if request.session.get('usuario'):
        email       = request.session['usuario']
        Logueado    = Usuario.objects.get(usuario=email)
        id_usuario  = Usuario.objects.get(usuario=email)
        CuentasBancarias = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario)            
        if request.method == 'POST':
            CuentaOrigen    = request.POST.get("CuentaOrigen")
            CuentaDestino   = request.POST.get("CuentaDestino")
            Descripcion     = request.POST.get("Descripcion")
            Password        = request.POST.get("password")
            Monto        = request.POST.get("MontoTransaccion")
            MontoTransaccion= request.POST.get("MontoTransaccion")
            if CuentaOrigen == '' or CuentaDestino == '' or Descripcion == '' or Password == '' or Monto == '' or MontoTransaccion == '':
                response_data = {}
                response_data['result'] = 'Error'
                response_data['message'] = 'Campos Vacios, Por favor llenar todos los campos'
                ps = pstats.Stats(pr, stream=sys.stdout)
                #ps.print_stats()
                pr.disable()
                pr.dump_stats('profile2.prof')
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            ##Para realizar una transaccion se realiza en dos operaciones
            ## 1- Se saca de la Cuenta Origen   -> En DebitoCredito se pone 0
            ## 2- Se carga en cuenta destino    -> En DebitoCredito se pone 5
            ## Esto para facilitar las consultas
                
            retorno_validacion = validar_transaccion(CuentaOrigen, CuentaDestino, Monto)
            if retorno_validacion == 1:
                CrearTransaccion(CuentaOrigen,CuentaDestino,0,Monto,Descripcion)
                CrearTransaccion(CuentaDestino,CuentaOrigen,5,Monto,Descripcion)
                response_data = {}
                response_data['result'] = 'Error'
                response_data['message'] = 'Operacion Realizada Satisfactoriaente!!'
                ps = pstats.Stats(pr, stream=sys.stdout)
                #ps.print_stats()
                pr.disable()
                pr.dump_stats('profile2.prof')
                return HttpResponse(json.dumps(response_data), content_type="application/json")                
            elif retorno_validacion == 2:
                response_data = {}
                response_data['result'] = 'Error'
                response_data['message'] = 'No se se tiene suficiente saldo para la transaccion'
                ps = pstats.Stats(pr, stream=sys.stdout)
                #ps.print_stats()
                pr.disable()
                pr.dump_stats('profile2.prof')
                return HttpResponse(json.dumps(response_data), content_type="application/json")
            elif retorno_validacion == 3:
                response_data = {}
                response_data['result'] = 'Error'
                response_data['message'] = 'Error La cuenta Destino no existe'
                ps = pstats.Stats(pr, stream=sys.stdout)
                #ps.print_stats()
                pr.disable()
                pr.dump_stats('profile2.prof')
                return HttpResponse(json.dumps(response_data), content_type="application/json")
        response_data = {}
        response_data['result'] = 'Error'
        response_data['message'] = 'Error en Operacion'
        ps = pstats.Stats(pr, stream=sys.stdout)
        #ps.print_stats()
        pr.disable()
        pr.dump_stats('profile2.prof')
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        response_data = {}
        response_data['result'] = 'Error'
        response_data['message'] = 'Error de Autenticacion'
        ps = pstats.Stats(pr, stream=sys.stdout)
        #ps.print_stats()
        pr.disable()
        pr.dump_stats('profile2.prof')
        return HttpResponse(json.dumps(response_data), content_type="application/json")

@csrf_exempt
def VerHistorialCuenta(request):
    pr = cProfile.Profile()
    pr.enable()
    if request.method == 'POST':
        cuenta        = request.POST.get("cuenta")
        if request.session.get('usuario'):
            username        = request.session['usuario']
            id_usuario      = Usuario.objects.get(usuario=username)
            Cuenta          = CuentaBancaria.objects.all().filter(NumeroCuentaBancaria=cuenta).last()
            Transacciones   = Transaccion.objects.all().filter(CuentaOrigen=Cuenta)
            template_name   = 'transacciones/HistorialTransacciones.html'
            ps = pstats.Stats(pr, stream=sys.stdout)
            #ps.print_stats()
            pr.disable()
            pr.dump_stats('profile2.prof')
            return render(request, template_name,{'persona': id_usuario, 'Transacciones': Transacciones})   
        
        else:
            ps = pstats.Stats(pr, stream=sys.stdout)
            #ps.print_stats()
            pr.disable()
            pr.dump_stats('profile2.prof')
            return  HttpResponseRedirect('/inicio')
    else:
        ps = pstats.Stats(pr, stream=sys.stdout)
        #ps.print_stats()
        pr.disable()
        pr.dump_stats('profile2.prof')
        return  HttpResponseRedirect('/inicio')

def validar_transaccion(CuentaOrigen, CuentaDestino, Monto):
    if ExisteCuenta(CuentaDestino) == False:
        return 3
    if Valida(CuentaOrigen, Monto) == False:
        return 2
    return 1

def ExisteCuenta(Cuenta):
    existe = CuentaBancaria.objects.filter(NumeroCuentaBancaria=Cuenta).exists()
    return existe

def Valida(cta, monto):
    Cuenta = CuentaBancaria.objects.all().filter(NumeroCuentaBancaria=cta).last()
    if float(Cuenta.saldo) >= float(monto):
        return True
    else:
        return False


def HistorialTransacciones(request):
    if request.session.get('usuario'):
        username        = request.session['usuario']
        id_usuario      = Usuario.objects.get(usuario=username)
        Cuenta          = CuentaBancaria.objects.all().filter(UsuarioPropietario=id_usuario).last()
        Transacciones   = Transaccion.objects.all().filter(CuentaOrigen=Cuenta)
        template_name   = 'transacciones/HistorialTransacciones.html'
        return render(request, template_name,{'persona': id_usuario, 'Transacciones': Transacciones})   
    
    else:
        return  HttpResponseRedirect('/inicio')
    

def CrearTransaccion(CuentaOrigen,CuentaDestino,DebitoCredito,Monto,Descripcion):
    cta_origen = CuentaBancaria.objects.get(NumeroCuentaBancaria=CuentaOrigen)
    cta_destino = CuentaBancaria.objects.get(NumeroCuentaBancaria=CuentaDestino)
    if DebitoCredito == 0:
        cta_origen.saldo = float(cta_origen.saldo) - float(Monto)
        cta_destino.saldo = float(cta_destino.saldo) + float(Monto)
        cta_origen.save()
        cta_destino.save()

    trx = Transaccion()
    trx.id              = randint(1000000, 9000000)
    trx.CuentaOrigen    = cta_origen
    trx.CuentaDestino   = cta_destino
    trx.DebitoCredito   = DebitoCredito
    trx.Monto           = Monto
    trx.Decripcion      = Descripcion
    trx.FechaTransaccion=timezone.now()
    trx.save()
    return trx


def PracticaAnalisis(request):
    return render(request, 'transacciones/analisis.html')
