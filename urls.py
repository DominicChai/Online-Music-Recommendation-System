from django.urls import path
from . import views
app_name='polls'
from django.conf.urls import include, url
#path:（定义了url的格式，对应的视图是什么并且调用view种对应的函数，obj的名字）
from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('register/', views.register, name='register'),
    path('login/', views.my_login, name='my_login'),
    path('logout/', views.my_logout, name='my_logout'),
    path('login_success/', views.login_success, name='my_logout'),
    path('get_songs/', views.get_songs, name='get_songs'),
    path('ajax_demo/', views.ajax_demo),
    path('demo_add/', views.demo_add),
    path('getdata/', views.getdata),
    path('song_add/',views.addsong),
path('main_page/',views.main_page),
path('song_play/',views.song_play),
path('recommand/',views.recommand),
path('managesong/',views.managesong),
    path('splitpage/',views.splitpage),
path('mark/',views.mark),

]
#可以增加很多种url的模式 一种url pattern就对应可以return一种view
