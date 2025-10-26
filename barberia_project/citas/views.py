from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, time, timedelta
from dateutil.parser import parse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .forms import CitaForm
from .models import Cita, Servicio
import json
from django.utils.safestring import mark_safe

@login_required
def agendar_cita_view(request):
    if request.method == 'POST':
        form = CitaForm(request.POST)
        if form.is_valid():
            cita = form.save(commit=False)
            cita.usuario = request.user
            cita.save()
            form.save_m2m()
            
            return redirect('citas:cita_confirmada', cita_id=cita.id)
    else:

        user_full_name = request.user.get_full_name()
        if not user_full_name:
            user_full_name = request.user.username
        
        initial_data = {'nombre_cliente': user_full_name}
        form = CitaForm(initial=initial_data)

        servicios = Servicio.objects.all()

    precios_servicios_dict = {
        str(s.id): float(s.precio) for s in Servicio.objects.all()
    }
    precios_json = json.dumps(precios_servicios_dict)
    
    duraciones_servicios_dict = {str(s.id): s.duracion_minutos for s in servicios}
    duraciones_json = json.dumps(duraciones_servicios_dict)
    
    context = {
        'form': form,
        'precios_servicios_json': mark_safe(precios_json), 
        'duraciones_servicios_json': mark_safe(duraciones_json), 
    }
    
    return render(request, 'citas/agendar_cita.html', context)

def obtener_horas_disponibles(request):
    fecha_str = request.GET.get('fecha')
    
    servicios_csv = request.GET.get('servicios')

    if not fecha_str or not servicios_csv:
        return JsonResponse({'error': 'Faltan datos (Fecha y al menos un Servicio).'}, status=400)

    try:
        servicios_ids = servicios_csv.split(',') 
        fecha_seleccionada = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        servicios_seleccionados = Servicio.objects.filter(pk__in=servicios_ids)
        
        if not servicios_seleccionados.exists():
            return JsonResponse({'error': 'Servicios no válidos.'}, status=400)
        
        duracion_total_nueva_cita = sum(s.duracion_minutos for s in servicios_seleccionados)
        
    except (ValueError, Servicio.DoesNotExist):
        return JsonResponse({'error': 'Formato de datos inválido.'}, status=400)

    HORA_INICIO, HORA_FIN, INTERVALO_MINUTOS = 10, 22, 30
    horas_disponibles = []
    citas_del_dia = Cita.objects.filter(
        fecha_hora_inicio__date=fecha_seleccionada
    ).exclude(
        estado='CANCELADA'
    ).prefetch_related('servicios')
    
    hora_actual = datetime.combine(fecha_seleccionada, time(HORA_INICIO, 0))
    hora_limite = datetime.combine(fecha_seleccionada, time(HORA_FIN, 0))

    while hora_actual + timedelta(minutes=duracion_total_nueva_cita) <= hora_limite:
        slot_inicio = timezone.make_aware(hora_actual)
        slot_fin = slot_inicio + timedelta(minutes=duracion_total_nueva_cita)
        
        reservada = False
        for cita_existente in citas_del_dia:
            if cita_existente.fecha_hora_fin and slot_inicio < cita_existente.fecha_hora_fin and slot_fin > cita_existente.fecha_hora_inicio:
                reservada = True
                break

        horas_disponibles.append({
            'hora': hora_actual.strftime('%I:%M %p'),
            'reservada': reservada,
            'formato_db': slot_inicio.isoformat()
        })
        hora_actual += timedelta(minutes=INTERVALO_MINUTOS)

    return JsonResponse({'horas': horas_disponibles})

def cita_confirmada_view(request, cita_id):
    try:
        cita = Cita.objects.get(id=cita_id)
    except Cita.DoesNotExist:
        return redirect('home') 
        
    return render(request, 'citas/cita_confirmada.html', {'cita': cita})

@staff_member_required
def lista_citas_view(request):
    todas_las_citas = Cita.objects.all().order_by('-fecha_hora_inicio').prefetch_related('servicios')
    
    context = {
        'citas': todas_las_citas
    }
    
    return render(request, 'citas/lista_citas.html', context)