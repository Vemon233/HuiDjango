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
    pathogens_new = []
    i = 0
    for pathogen in pathogens:
        str_name = pathogen[0]
        str_name = str_name.replace('_', ' ')
        pa = list(pathogens[i])
        pa.append(str_name)
        pathogens_new.append(pa)
        i += 1
    print(pathogens_new)
    context_dict['pathogens'] = pathogens_new
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
    pathogens_new = []
    i = 0
    for pathogen in pathogens:
        str_name = pathogen[0]
        str_name = str_name.replace('_', ' ')
        pa = list(pathogens[i])
        pa.append(str_name)
        pathogens_new.append(pa)
        i += 1
    context_dict['pathogens'] = pathogens_new
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
    pathogens_new = []
    i = 0
    for pathogen in pathogens:
        str_name = pathogen[0]
        str_name = str_name.replace('_', ' ')
        pa = list(pathogens[i])
        pa.append(str_name)
        pathogens_new.append(pa)
        i += 1
    context_dict['pathogens'] = pathogens_new
    context_dict['list_name'] = "rare disease"
    return render(request, 'list.html', context_dict)


def search(request):
    context_dict = {}
    search_word = request.GET.get('search_word', '')
    search_pathogen = Disease.objects.filter(name__icontains=search_word)
    search_pathogen = search_pathogen.values('name').distinct()
    pathogen_name = []
    for pathogen in search_pathogen:
        pa = []
        pa.append(pathogen['name'])
        str_name = pathogen['name']
        str_name = str_name.replace('_', ' ')
        pa.append(str_name)
        pathogen_name.append(pa)
    context_dict['search_word'] = search_word
    context_dict['pathogens'] = pathogen_name
    return render(request, 'search.html', context_dict)


def singledi(request, di_name):
    context_dict = {}
    try:
        disease = Disease.objects.filter(name=di_name)
        di_name = di_name.replace('_', ' ')
        context_dict['disease'] = disease
        context_dict['name'] = di_name
    except Disease.DoesNotExist:
        context_dict['disease'] = None
        context_dict['name'] = di_name
    return render(request, 'single_pathogen.html', context_dict)
