import pymysql
from django.shortcuts import render
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
    return render(request, 'board.html', context_dict)


def undiagnosed(request):
    context_dict = {}
    return render(request, 'undiagnosed.html', context_dict)


def list_frequent(request):
    context_dict = {}

    conn = pymysql.connect(
        host='localhost',
        port=3306,
        charset='UTF8',
        user='root',
        password='521365zhh',
        db='diseasedb'
    )
    cur = conn.cursor()

    sqlQuery = '''
    SELECT name, sum(cases)
    from disease
    where class = 'frequent'
    group by name
    order by sum(cases)
    '''
    name_list = []
    cases_list = []
    try:
        cur.execute(sqlQuery)
        results = cur.fetchall()
        for row in results:
            name_list.append(row[0])
            cases_list.append(row[1])
    except pymysql.Error as e:
        print("Failed: " + str(e))
    finally:
        cur.close()
        conn.close()

    context_dict['pathogens'] = name_list
    context_dict['cases_list'] = cases_list

    return render(request, 'list_frequent.html', context_dict)
