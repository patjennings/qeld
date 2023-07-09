from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

# Create your views here.
def matchs(request):
    template = loader.get_template('matchs.html')
    context = {
        'title': 'Qeld est lancé',
        'message': 'Qeld permet de gérer les matchs d\'une saison',
    }
    return HttpResponse(template.render(context, request))
