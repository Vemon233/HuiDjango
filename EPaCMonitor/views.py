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


def pathogen(request):
    context_dict = {}
    return render(request, 'pathogen.html', context_dict)


def board(request):
    context_dict = {}
    return render(request, 'list.html', context_dict)


def undiagnosed(request):
    context_dict = {}
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
    return render(request, 'list.html', context_dict)

