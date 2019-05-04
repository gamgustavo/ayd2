from django.db import models

# Create your models here.
class Cuenta(models.Model):
    id = models.IntegerField(primary_key=True)
    usuario = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    saldo = models.IntegerField()
    def __str__(self):
        return self.usuario


class Usuario(models.Model):
    id = models.IntegerField(primary_key=True)    
    usuario = models.CharField(max_length=150)    
    Nombre = models.CharField(max_length=150)
    Apellido = models.CharField(max_length=150)        
    password = models.CharField(max_length=150)
    direccion = models.CharField(max_length=150)
    telefono = models.IntegerField()        
    Fecha_Creacion = models.DateField(null=True)
    FechaFin = models.DateField(null=True)
    def __str__(self):
        return self.usuario

class CuentaBancaria(models.Model):
    NumeroCuentaBancaria = models.IntegerField(primary_key=True)
    UsuarioPropietario = models.ForeignKey(Usuario,related_name='CuentaBancariaUsuario', on_delete=models.CASCADE)
    saldo = models.DecimalField(max_digits=8, decimal_places=4)
    FechaInicio = models.DateField(null=True)
    FechaFin = models.DateField(null=True)    
    def __str__(self):
        return self.UsuarioPropietario

class ServiciosBancarios(models.Model):
    id = models.IntegerField(primary_key=True)
    Usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    NumeroCuentaBancaria = models.ForeignKey(CuentaBancaria, on_delete=models.CASCADE)
    NombreServicio = models.CharField(max_length=150)
    FechaInicio = models.DateField(null=True)
    FechaFin = models.DateField(null=True)        
    def __str__(self):
        return self.NombreServicio


class Transaccion(models.Model):
    id = models.IntegerField(primary_key=True)
    CuentaOrigen = models.ForeignKey(CuentaBancaria,related_name='OrigenCuenta', on_delete=models.CASCADE)
    CuentaDestino = models.ForeignKey(CuentaBancaria,related_name='DestinoCuenta', on_delete=models.CASCADE)
    DebitoCredito = models.IntegerField() ##  5 = Debito (Se agrega a cuenta) | 0 = Credito (Se quita a cuenta)
    Monto = models.DecimalField(max_digits=8, decimal_places=4)
    Decripcion = models.CharField(max_length=150)
    FechaTransaccion = models.DateField(null=True)
    def __str__(self):
        return self.CuentaOrigen