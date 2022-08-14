from django.urls import path
from EPaCMonitor import views

app_name = 'EPaCMonitor'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('undiagnosed/', views.undiagnosed, name='undiagnosed'),
    path('list_lowest/', views.list_lowest, name='list_lowest'),
    path('list_low/', views.list_low, name='list_low'),
    path('list_medium/', views.list_medium, name='list_medium'),
    path('list_high/', views.list_high, name='list_high'),
    path('search/', views.search, name='search'),
    path('disease/<di_name>/', views.singledi, name='post'),
]
