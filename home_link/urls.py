from django.urls import path

from . import views

app_name = 'home_link'

urlpatterns = [
    # django 会从用户访问的 URL 中自动提取 URL 路径参数转换器 <type:name> 规则捕获的值，然后传递给其对应的视图函数。
    path('grade/', views.grade_index, name='grade_index'),

    # 爬取新网址时用
    path('spider/', views.house_spider, name='house_spider'),

    path('predict/', views.house_yuce, name='house_yuce'),
    path('pre/', views.yuce_index, name='yuce_index'),
    path('', views.wel_index, name='wel_index')
]