from django.urls import path
from EPaCMonitor import views

app_name = 'EPaCMonitor'

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('board/', views.board, name='board'),
    path('pathogen/', views.pathogen, name='pathogen'),
    path('undiagnosed/', views.undiagnosed, name='undiagnosed'),
    path('list_frequent/', views.list_frequent, name='list_frequent'),
]
