from django.shortcuts import render
from .models import Corte
from django.core.paginator import Paginator

def lista_cortes(request):
    lista_de_cortes_completa = Corte.objects.all().order_by('-id') 

    paginator = Paginator(lista_de_cortes_completa, 8)

    page_number = request.GET.get('page')
    
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj 
    }
    
    return render(request, 'galeria/lista_cortes.html', context)