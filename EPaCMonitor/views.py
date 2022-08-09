from django.shortcuts import render
from django.db import connection
from EPaCMonitor.models import Disease


# Create your views here.
def index(request):
    context_dict = {}
    return render(request, 'index.html', context_dict)


def about(request):
    context_dict = {}
    return render(request, 'about.html', context_dict)


def undiagnosed(request):
    context_dict = {}
    context_dict['pathogen_name'] = "Undiagnosed pathogens"
    context_dict['danger_level'] = "unknown"
    return render(request, 'undiagnosed.html', context_dict)


def list_frequent(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name, sum(cases)
        from disease
        where class = 'frequent'
        group by name
        order by sum(cases)
        '''

    cur.execute(sqlQuery)
    result = cur.fetchall()
    pathogens = list(result)
    cur.close()
    pathogens.reverse()
    context_dict['pathogens'] = pathogens
    context_dict['list_name'] = "frequent disease"
    return render(request, 'list.html', context_dict)


def list_common(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name, sum(cases)
        from disease
        where class = 'common'
        group by name
        order by sum(cases)
        '''

    cur.execute(sqlQuery)
    result = cur.fetchall()
    pathogens = list(result)
    cur.close()
    pathogens.reverse()
    context_dict['pathogens'] = pathogens
    context_dict['list_name'] = "common disease"
    return render(request, 'list.html', context_dict)


def list_less(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name, sum(cases)
        from disease
        where class = 'less'
        group by name
        order by sum(cases)
        '''

    cur.execute(sqlQuery)
    result = cur.fetchall()
    pathogens = list(result)
    cur.close()
    pathogens.reverse()
    context_dict['pathogens'] = pathogens
    context_dict['list_name'] = "rare disease"
    return render(request, 'list.html', context_dict)


def search(request):
    context_dict = {}
    search_word = request.GET.get('search_word', '')
    search_pathogen = Disease.objects.filter(name__icontains=search_word)
    search_pathogen = search_pathogen.values('name').distinct()
    context_dict['search_word'] = search_word
    context_dict['pathogens'] = search_pathogen
    return render(request, 'search.html', context_dict)
