import pymysql
import datetime
import pyecharts.options as opts
from pyecharts.charts import Line
from pyecharts.charts import Map
from pyecharts.charts import Pie

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

sqlQuery = "SELECT * FROM disease WHERE class = 'undiagnosed'"
try:
    cur.execute(sqlQuery)
    results = cur.fetchall()
    for row in results:
        di_id_list.append(row[0])
        di_name_list.append(row[1])
        di_date_list.append(row[2])
        di_country_list.append(row[3])
        di_cases_list.append(row[4])
        di_class_list.append(row[5])
except pymysql.Error as e:
    print("Failed: "+str(e))

print(len(di_id_list))
# print('1')
# print(len(di_id_list))
# print(di_id_list)
# print('2')
# print(len(di_name_list))
# print(di_name_list)
# print('3')
# print(len(di_date_list))
# print(di_date_list)
# print('4')
# print(len(di_country_add_list))
# print(di_country_add_list)
# print('5')
# print(len(di_cases_list))
# print(di_cases_list)
# print('6')
# print(len(di_class_list))
# print(di_class_list)

# for line charts
x_data_list = []
y_data_list = [di_cases_list[0]]
y_add_data_list = [di_cases_list[0]]
for x in di_date_list:
    if x not in x_data_list:
        x_data_list.append(x)
print(x_data_list)
j = 0
case_num = di_cases_list[0]
for i in range(1, len(di_cases_list)):
    case_num = case_num + di_cases_list[i]
    if di_date_list[i] == di_date_list[i-1]:
        j = j + 1
        y_add_data_list[i-j] = case_num
    else:
        y_add_data_list.append(case_num)
k = 0
for i in range(1, len(di_cases_list)):
    if di_date_list[i] == di_date_list[i-1]:
        k = k + 1
        y_data_list[i-k] += di_cases_list[i]
    else:
        y_data_list.append(di_cases_list[i])
print(y_data_list)

x_list = []
y_list = []
y_add_list = []
day = x_data_list[0]
i = 0
case_num = 0
while day <= x_data_list[-1]:
    x_list.append(day)
    if day in x_data_list:
        case_num += y_add_data_list[i]
        y_list.append(y_data_list[i])
        i += 1
    else:
        y_list.append(0)
    y_add_list.append(case_num)
    day += datetime.timedelta(days=1)
print(x_list)
print(y_list)
print(y_add_list)

(
    Line()
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category", name="Date"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="Daily New Cases",
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
    .render("udhtml/line_chart_daily.html")
)

(
    Line()
    .set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category", name="Date"),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name="Total Cases",
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
    .render("udhtml/line_chart_total.html")
)

# for the world map
x_wm_list = di_country_list
y_wm_list = di_cases_list
wm_data = []
for index in range(len(x_wm_list)):
    city_ionfo = [di_country_list[index], di_cases_list[index]]
    wm_data.append(city_ionfo)

(
    Map()
    .add("Undiagnosed Disease", wm_data, "world", is_map_symbol_show=False)
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="Undiagnosed Disease Distribution Map"),
        visualmap_opts=opts.VisualMapOpts(max_=16),
    )
    .render("udhtml/map_world.html")
)

# for the pie chart
sqlQuery = '''
SELECT country, sum(cases)
from disease
where class = 'undiagnosed'
group by country
order by sum(cases)
'''
pie_country_list = []
pie_cases_list = []
try:
    cur.execute(sqlQuery)
    results = cur.fetchall()
    for row in results:
        pie_country_list.append(row[0])
        pie_cases_list.append(row[1])
except pymysql.Error as e:
    print("Failed: "+str(e))

pie_data = []
for index in range(len(pie_country_list)):
    pie_ionfo = [pie_country_list[index], pie_cases_list[index]]
    pie_data.append(pie_ionfo)
(
    Pie()
    .add("Cases by Country", pie_data)
    .set_global_opts(legend_opts=opts.LegendOpts(is_show=False))
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    .render("udhtml/pie_base.html")
)

cur.close()
conn.close()
