from django.db import models

# Modelo para los campistas
class Campista(models.Model):
    nombre_completo = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.TextField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_completo


# Modelo para las reservas
class Reserva(models.Model):
    TIPO_ALOJAMIENTO_CHOICES = [
        ('Tienda', 'Tienda'),
        ('Cabaña', 'Cabaña'),
        ('Caravana', 'Caravana'),
    ]

    ESTADO_RESERVA_CHOICES = [
        ('Confirmada', 'Confirmada'),
        ('Pendiente', 'Pendiente'),
        ('Cancelada', 'Cancelada'),
    ]

    campista = models.ForeignKey(Campista, on_delete=models.CASCADE, related_name='reservas')
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    tipo_alojamiento = models.CharField(max_length=10, choices=TIPO_ALOJAMIENTO_CHOICES)
    numero_personas = models.PositiveIntegerField()
    estado_reserva = models.CharField(max_length=10, choices=ESTADO_RESERVA_CHOICES, default='Pendiente')
    observaciones = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Reserva de {self.campista.nombre_completo} ({self.tipo_alojamiento})"

    class Meta:
        ordering = ['-fecha_inicio']
