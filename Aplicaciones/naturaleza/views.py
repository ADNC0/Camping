from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Campista
from datetime import datetime
from .models import Reserva

def inicio(request):
    return render(request, 'inicio.html')

# ---------------------------
# Vistas para Campista
# ---------------------------
def listadoCampistas(request):
    campistas = Campista.objects.all()
    return render(request, "campista/listadoCampista.html", {'campistas': campistas})

def nuevaCampista(request):
    return render(request, 'campista/nuevaCampista.html')

def guardarCampista(request):
    if request.method == 'POST':
        nombre_completo = request.POST.get('nombre_completo')
        correo_electronico = request.POST.get('correo_electronico')
        telefono = request.POST.get('telefono')
        direccion = request.POST.get('direccion', '')
        fecha_registro = request.POST.get('fecha_registro')

        errors = {}
        if not nombre_completo:
            errors['nombre_completo'] = "El nombre completo es obligatorio."
        if not correo_electronico:
            errors['correo_electronico'] = "El correo electrónico es obligatorio."
        if not telefono:
            errors['telefono'] = "El teléfono es obligatorio."
        if not fecha_registro:
            errors['fecha_registro'] = "La fecha de registro es obligatoria."

        if errors:
            for field, error_msg in errors.items():
                messages.error(request, f"{error_msg}")
            return redirect('nuevoCampista')

        if fecha_registro:
            fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date()
            if fecha_registro < datetime.now().date():
                messages.error(request, "La fecha de registro no puede ser anterior a la fecha actual.")
                return redirect('nuevoCampista')

        Campista.objects.create(
            nombre_completo=nombre_completo,
            correo_electronico=correo_electronico,
            telefono=telefono,
            direccion=direccion,
            fecha_registro=fecha_registro or datetime.now().date(),
        )

        messages.success(request, "Campista creado exitosamente.")
        return redirect('listado_campistas')

    else:
        messages.error(request, "Método no permitido.")
        return redirect('nuevoCampista')

def editarCampista(request, id):
    campistaEditar = get_object_or_404(Campista, id=id)
    return render(request, 'campista/editarCampista.html', {'campistaEditar': campistaEditar})

def procesoActualizarCampista(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        campista = get_object_or_404(Campista, id=id)

        campista.nombre_completo = request.POST.get('nombre_completo')
        campista.correo_electronico = request.POST.get('correo_electronico')
        campista.telefono = request.POST.get('telefono')
        campista.direccion = request.POST.get('direccion')

        fecha_registro = request.POST.get('fecha_registro')
        if fecha_registro:
            try:
                fecha_registro = datetime.strptime(fecha_registro, '%Y-%m-%d').date()
                if fecha_registro < datetime.now().date():
                    messages.error(request, "La fecha de registro no puede ser anterior a la fecha actual.")
                    return redirect('editarCampista', id=id)
                campista.fecha_registro = fecha_registro
            except ValueError:
                messages.error(request, "La fecha de registro es inválida.")
                return redirect('editarCampista', id=id)

        campista.save()
        messages.success(request, "Campista actualizado correctamente.")
        return redirect('listado_campistas')
    else:
        messages.error(request, "Método no permitido.")
        return redirect('listado_campistas')

def eliminarCampista(request, id):
    campistaEliminar = get_object_or_404(Campista, id=id)
    campistaEliminar.delete()
    messages.success(request, "Campista eliminado exitosamente.")
    return redirect('listado_campistas')


# ---------------------------
# Vistas para Reserva
# ---------------------------

def listadoReservas(request):
    reservas = Reserva.objects.all()
    return render(request, "reserva/listadoReserva.html", {'reservas': reservas})

def nuevaReserva(request):
    campistas = Campista.objects.all()
    return render(request, 'reserva/nuevaReserva.html', {'campistas': campistas})

def guardarReserva(request):
    if request.method == 'POST':
        try:
            campista_id = request.POST.get('campista')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            tipo_alojamiento = request.POST.get('tipo_alojamiento')
            numero_personas = request.POST.get('numero_personas')
            estado_reserva = request.POST.get('estado_reserva')
            observaciones = request.POST.get('observaciones', '')

            if not campista_id or not fecha_inicio or not fecha_fin or not tipo_alojamiento or not numero_personas or not estado_reserva:
                messages.error(request, "Todos los campos obligatorios deben ser completados.")
                return redirect('nuevaReserva')

            try:
                fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
                fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()

                if fecha_inicio < datetime.now().date():
                    messages.error(request, "La fecha de inicio no puede ser anterior a la fecha actual.")
                    return redirect('nuevaReserva')

                if fecha_fin < fecha_inicio:
                    messages.error(request, "La fecha de fin no puede ser anterior a la fecha de inicio.")
                    return redirect('nuevaReserva')
            except ValueError:
                messages.error(request, "Formato de fecha inválido.")
                return redirect('nuevaReserva')

            try:
                campista = Campista.objects.get(id=campista_id)
            except Campista.DoesNotExist:
                messages.error(request, "Campista no encontrado.")
                return redirect('nuevaReserva')

            reserva = Reserva.objects.create(
                campista=campista,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo_alojamiento=tipo_alojamiento,
                numero_personas=numero_personas,
                estado_reserva=estado_reserva,
                observaciones=observaciones,
            )

            messages.success(request, "Reserva creada exitosamente.")
            return redirect('listado_reservas')

        except Exception as e:
            messages.error(request, f"Hubo un error inesperado: {str(e)}")
            return redirect('nuevaReserva')

    else:
        messages.error(request, "Método no permitido.")
        return redirect('nuevaReserva')

def editarReserva(request, id):
    reservaEditar = get_object_or_404(Reserva, id=id)
    campistas = Campista.objects.all()

    if request.method == 'POST':
        reservaEditar.campista = Campista.objects.get(id=request.POST.get('campista'))
        reservaEditar.fecha_inicio = request.POST.get('fecha_inicio')
        reservaEditar.fecha_fin = request.POST.get('fecha_fin')
        reservaEditar.tipo_alojamiento = request.POST.get('tipo_alojamiento')
        reservaEditar.numero_personas = request.POST.get('numero_personas')
        reservaEditar.estado_reserva = request.POST.get('estado_reserva')
        reservaEditar.observaciones = request.POST.get('observaciones')

        try:
            fecha_inicio = datetime.strptime(reservaEditar.fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(reservaEditar.fecha_fin, '%Y-%m-%d').date()

            if fecha_inicio < datetime.now().date():
                messages.error(request, "La fecha de inicio no puede ser anterior a la fecha actual.")
                return redirect('editarReserva', id=id)

            if fecha_fin < fecha_inicio:
                messages.error(request, "La fecha de fin no puede ser anterior a la fecha de inicio.")
                return redirect('editarReserva', id=id)
        except ValueError:
            messages.error(request, "Formato de fecha inválido.")
            return redirect('editarReserva', id=id)

        reservaEditar.save()
        messages.success(request, "Reserva actualizada exitosamente.")
        return redirect('listado_reservas')

    return render(request, 'reserva/editarReserva.html', {
        'reservaEditar': reservaEditar,
        'campistas': campistas,
    })

def procesoActualizarReserva(request):
    if request.method == 'POST':
        id = request.POST.get('id')
        reserva = get_object_or_404(Reserva, id=id)

        reserva.campista = Campista.objects.get(id=request.POST.get('campista'))
        reserva.fecha_inicio = request.POST.get('fecha_inicio')
        reserva.fecha_fin = request.POST.get('fecha_fin')
        reserva.tipo_alojamiento = request.POST.get('tipo_alojamiento')
        reserva.numero_personas = request.POST.get('numero_personas')
        reserva.estado_reserva = request.POST.get('estado_reserva')
        reserva.observaciones = request.POST.get('observaciones')

        try:
            fecha_inicio = datetime.strptime(reserva.fecha_inicio, '%Y-%m-%d').date()
            fecha_fin = datetime.strptime(reserva.fecha_fin, '%Y-%m-%d').date()

            if fecha_inicio < datetime.now().date():
                messages.error(request, "La fecha de inicio no puede ser anterior a la fecha actual.")
                return redirect('editarReserva', id=id)

            if fecha_fin < fecha_inicio:
                messages.error(request, "La fecha de fin no puede ser anterior a la fecha de inicio.")
                return redirect('editarReserva', id=id)

            reserva.save()
            messages.success(request, "Reserva actualizada correctamente.")
            return redirect('listado_reservas')

        except ValueError:
            messages.error(request, "El formato de las fechas es incorrecto.")
            return redirect('editarReserva', id=id)

    else:
        messages.error(request, "Método no permitido.")
        return redirect('listado_reservas')

def eliminarReserva(request, id):
    reservaEliminar = get_object_or_404(Reserva, id=id)
    reservaEliminar.delete()
    messages.success(request, "Reserva eliminada exitosamente.")
    return redirect('listado_reservas')
