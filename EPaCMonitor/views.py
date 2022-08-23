from django.shortcuts import render
from django.db import connection
from lxml import etree

from EPaCMonitor.models import Disease

import pymysql
import datetime
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.charts import Map
from pyecharts.charts import Pie


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


def list_high(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name, class, sum(cases)
        from disease
        where class = 'Highest'
        or class = 'High'
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
    context_dict['list_name'] = "danger disease"
    return render(request, 'list.html', context_dict)


def list_medium(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name,class, sum(cases)
        from disease
        where class = 'Medium'
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


def list_low(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name,class, sum(cases)
        from disease
        where class = 'Low'
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
    context_dict['list_name'] = "uncommon disease"
    return render(request, 'list.html', context_dict)


def list_lowest(request):
    context_dict = {}
    cur = connection.cursor()
    sqlQuery = '''
        SELECT name,class, sum(cases)
        from disease
        where class = 'Lowest'
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
    disease = Disease.objects.filter(name=di_name)

    if disease:
        filewriter = open('templates/single_pathogen.html', 'w')
        filewriter.write('''{% extends 'pathogen.html' %}
        
{% block title_title_block %}
    {{ name }}
{% endblock %}

{% block level_block %}
    {{ danger_level }}
{% endblock %}

{% block name_block %}{{ name }}{% endblock %}

        ''')
        filewriter.write("{% block line_total_block %}")

        conn = pymysql.connect(
            host='localhost',
            port=3306,
            charset='UTF8',
            user='root',
            password='521365zhh',
            db='diseasedb'
        )
        cur = conn.cursor()

        di_id_list = []
        di_name_list = []
        di_date_list = []
        di_country_list = []
        di_cases_list = []
        di_class_list = []

        sqlQuery = "SELECT * FROM disease WHERE name = %s"

        try:
            cur.execute(sqlQuery, di_name)
            results = cur.fetchall()
            for row in results:
                di_id_list.append(row[0])
                di_name_list.append(row[1])
                di_date_list.append(row[2])
                di_country_list.append(row[3])
                di_cases_list.append(row[4])
                di_class_list.append(row[5])
        except pymysql.Error as e:
            print("Failed: " + str(e))

        #count the danger level

        # posts_per_month = 0
        # for i in range(1, len(di_id_list)-1):
        #     posts = len(di_id_list) - i
        #     days = (di_date_list[-1]-di_date_list[i]).days
        #     months = days/30
        #     ppm = posts/months
        #     if ppm > posts_per_month:
        #         posts_per_month = ppm
        #     i += 1
        posts = len(di_date_list)
        days = (di_date_list[-1] - di_date_list[0]).days
        months = days / 30
        posts_per_month = posts / months
        print(posts_per_month)
        danger_level = ''
        if posts_per_month > 10:
            danger_level = 'Highest'
        elif posts_per_month > 6:
            danger_level = 'High'
        elif posts_per_month > 4:
            danger_level = 'Medium'
        elif posts_per_month > 2:
            danger_level = 'Low'
        else:
            danger_level = 'Lowest'






        x_data_list = []
        y_data_list = [di_cases_list[0]]
        y_add_data_list = [di_cases_list[0]]
        for x in di_date_list:
            if x not in x_data_list:
                x_data_list.append(x)
        j = 0
        case_num = di_cases_list[0]
        for i in range(1, len(di_cases_list)):
            case_num = case_num + di_cases_list[i]
            if di_date_list[i] == di_date_list[i - 1]:
                j = j + 1
                y_add_data_list[i - j] = case_num
            else:
                y_add_data_list.append(case_num)
        k = 0
        for i in range(1, len(di_cases_list)):
            if di_date_list[i] == di_date_list[i - 1]:
                k = k + 1
                y_data_list[i - k] += di_cases_list[i]
            else:
                y_data_list.append(di_cases_list[i])

        x_list = []
        y_list = []
        y_add_list = []
        day = x_data_list[0]
        i = 0
        case_num = 0
        while day <= x_data_list[-1]:
            x_list.append(day)
            if day in x_data_list:
                y_list.append(y_data_list[i])
                i += 1
            else:
                y_list.append(0)
            day += datetime.timedelta(days=1)

        i = 0
        day = x_data_list[0]
        while day <= x_data_list[-1]:
            case_num += y_list[i]
            i += 1
            y_add_list.append(case_num)
            day += datetime.timedelta(days=1)

        (
            Line()
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category", name="Date"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    name="Total Activities",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
                .add_xaxis(xaxis_data=x_list)
                .add_yaxis(
                series_name="",
                y_axis=y_add_list,
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .render("templates/single_page/line_chart_total.html")
        )
        fo = open('templates/single_page/line_chart_total.html', 'r', encoding='utf-8')
        iter_f = iter(fo)
        file_str = []
        for line in iter_f:
            file_str.append(line)
        file_str = file_str[9:-2]
        for file_single_str in file_str:
            filewriter.write(file_single_str)

        filewriter.write('''
        {% endblock %}
        
        {% block line_daily_block %}
                ''')

        (
            Line()
                .set_global_opts(
                tooltip_opts=opts.TooltipOpts(is_show=False),
                xaxis_opts=opts.AxisOpts(type_="category", name="Date"),
                yaxis_opts=opts.AxisOpts(
                    type_="value",
                    name="Daily New Activities",
                    axistick_opts=opts.AxisTickOpts(is_show=True),
                    splitline_opts=opts.SplitLineOpts(is_show=True),
                ),
            )
                .add_xaxis(xaxis_data=x_list)
                .add_yaxis(
                series_name="",
                y_axis=y_list,
                symbol="emptyCircle",
                is_symbol_show=True,
                label_opts=opts.LabelOpts(is_show=False),
            )
                .render("templates/single_page/line_chart_daily.html")
        )



        fo = open('templates/single_page/line_chart_daily.html', 'r', encoding='utf-8')
        iter_f = iter(fo)
        file_str = []
        for line in iter_f:
            file_str.append(line)
        file_str = file_str[9:-2]
        for file_single_str in file_str:
            filewriter.write(file_single_str)

        filewriter.write('''
        {% endblock %}
        
        {% block world_map_block %}
                ''')


        # for the world map
        x_wm_list = di_country_list
        y_wm_list = di_cases_list
        wm_data = []
        for index in range(len(x_wm_list)):
            city_ionfo = [di_country_list[index], di_cases_list[index]]
            wm_data.append(city_ionfo)

        (
            Map(init_opts=opts.InitOpts(width="600px",height="300px"))
                .add(di_name, wm_data, "world", is_map_symbol_show=False)
                .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
                .set_global_opts(
                title_opts=opts.TitleOpts(title=di_name),
                visualmap_opts=opts.VisualMapOpts(max_=10),
            )
                .render("templates/single_page/map_world.html")
        )

        fo = open('templates/single_page/map_world.html', 'r', encoding='utf-8')
        iter_f = iter(fo)
        file_str = []
        for line in iter_f:
            file_str.append(line)
        file_str = file_str[10:-2]
        for file_single_str in file_str:
            filewriter.write(file_single_str)

        filewriter.write('''
        {% endblock %}

        {% block pie_block %}
                ''')

        # for the pie chart
        sqlQuery = '''
        SELECT country, sum(cases)
        from disease
        where name = %s
        group by country
        order by sum(cases)
        '''
        pie_country_list = []
        pie_cases_list = []
        try:
            cur.execute(sqlQuery, di_name)
            results = cur.fetchall()
            for row in results:
                pie_country_list.append(row[0])
                pie_cases_list.append(row[1])
        except pymysql.Error as e:
            print("Failed: " + str(e))

        pie_data = []
        for index in range(len(pie_country_list)):
            pie_ionfo = [pie_country_list[index], pie_cases_list[index]]
            pie_data.append(pie_ionfo)
        (
            Pie(init_opts=opts.InitOpts(width="400px",height="300px"))
                .add("Posts", pie_data)
                .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
                .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
                .render("templates/single_page/pie_base.html")
        )
        fo = open('templates/single_page/pie_base.html', 'r', encoding='utf-8')
        iter_f = iter(fo)
        file_str = []
        for line in iter_f:
            file_str.append(line)
        file_str = file_str[9:-2]
        for file_single_str in file_str:
            filewriter.write(file_single_str)

        filewriter.write('''
        {% endblock %}
                ''')


        filewriter.close()
        cur.close()
        conn.close()



    else:
        di_name = 'Page Not Exist'
    di_name = di_name.replace('_', ' ')
    context_dict['disease'] = disease
    context_dict['name'] = di_name
    context_dict['danger_level'] = danger_level
    return render(request, 'single_pathogen.html', context_dict)
