from datetime import datetime, time, timedelta
from django.http import JsonResponse
from django.utils import timezone
from django.shortcuts import render
from citas.models import Servicio
from .models import InformacionGeneral

def index(request):
    servicios = Servicio.objects.all().order_by('nombre')

    try:
        info = InformacionGeneral.objects.latest('fecha_actualizacion')
    except InformacionGeneral.DoesNotExist:
        info = None
        
    context = {
        'servicios': servicios,
        'info': info 
    }
    return render(request, 'core/index.html', context)

def agendar_cita_view(request):
    if request.method == 'POST':
        form = TuCitaForm(request.POST) 
        fecha_hora_str = request.POST.get('fecha_hora')

        if form.is_valid() and fecha_hora_str:
            cita = form.save(commit=False)

            from dateutil.parser import parse
            from django.utils import timezone

            dt_cita = parse(fecha_hora_str)
            cita.fecha_hora = timezone.make_aware(dt_cita) 

            cita.usuario = request.user 
            cita.save()

            return redirect('cita_exitosa') 
    else:
        form = TuCitaForm()

    return render(request, 'agendar_cita.html', {'form': form})

def obtener_horas_disponibles(request):
    if request.method == 'GET':
        fecha_str = request.GET.get('fecha')
        if not fecha_str:
            return JsonResponse({'error': 'Fecha requerida'}, status=400)

        try:
            fecha_seleccionada = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        except ValueError:
            return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)


        HORA_INICIO = 10 
        HORA_FIN = 22   
        INTERVALO_MINUTOS = 60 

        horas_disponibles = []
        
        hora_actual = datetime.combine(fecha_seleccionada, time(HORA_INICIO, 0))
        hora_limite = datetime.combine(fecha_seleccionada, time(HORA_FIN, 0))
        
        while hora_actual < hora_limite:
            dt_inicio = timezone.make_aware(hora_actual)
            dt_fin = timezone.make_aware(hora_actual + timedelta(minutes=INTERVALO_MINUTOS))
            
            cita_existente = Cita.objects.filter(
                fecha_hora__gte=dt_inicio, 
                fecha_hora__lt=dt_fin 
            ).exists()

            horas_disponibles.append({
                'hora': hora_actual.strftime('%H:%M'), 
                'reservada': cita_existente,
                'formato_db': dt_inicio.isoformat() 
            })

            hora_actual += timedelta(minutes=INTERVALO_MINUTOS)

        return JsonResponse({'horas': horas_disponibles})

    return JsonResponse({'error': 'Método no permitido'}, status=405)