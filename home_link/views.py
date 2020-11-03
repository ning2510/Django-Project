from django.shortcuts import render
from .models import GradeInfo
from .forms import GradeChoiceForm, Grade
from django.core.paginator import Paginator
from django.http import HttpResponse,HttpResponseRedirect
from fake_useragent import UserAgent		#fake_useragent第三方库，来实现随机请求头
import requests
from bs4 import BeautifulSoup
import re
import unicodedata
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model

def wel_index(request):
    return render(request, 'home_link/wel.html')

def is_number(s):       #判断s是否为数字
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

name_list = list('1')
name_dict = {
    'https://www.ynpxrz.com/n1456209c1599.aspx': 2016,
    'http://www.zizzs.com/c/201706/17861.html': 2017,
    'http://www.gaosan.com/gaokao/217808.html': 2018,
    'https://www.gjw.cn/GaoKaoZiXun/964809-2.html': 2019,
    'http://www.gaosan.com/gaokao/64218.html': 2020
}

yuce = [-1]
f = open("shuju.txt", 'r')
yuce_dict = dict([i.strip().split('\t') for i in f])
f.close()

def grade_index(request):
    form = GradeChoiceForm()

    if name_list[0] in name_dict:
        #print(name_list[0])
        grade_list = GradeInfo.objects.filter(name=name_list[0]).order_by('add_date')
        paginator = Paginator(grade_list, 100)      #一页100条信息
        page = request.GET.get('page', '')
        page_obj = paginator.get_page(page)

        id = name_dict[name_list[0]]


        return render(request, 'home_link/index.html',
                      context={'page_obj': page_obj, 'paginator': paginator,
                       'is_paginated': True, 'form': form, 'year': name_dict[name_list[0]], 'id': id})
    else:
        return render(request, 'home_link/index.html', context={'form': form, 'id': 0})


    '''
    首先把 HTTP 请求传了进去，然后 render 根据第二个参数的值 home_link/index.html 找到这个模板文件并读取模板中的内容。
    之后 render 根据我们传入的 context 参数的值把模板中的变量替换为我们传递的变量的值，{{ page_obj }} 被替换成了 context 字典中 page_obj 对应的值，
    同理 {{ paginator }} 也被替换成相应的值。
    '''


def house_spider(request):
    if request.method == 'POST':
        form = GradeChoiceForm(request.POST)
        if form.is_valid():
            url = form.cleaned_data.get('url')

            name_list[0] = url

            #home_spider = HomeLinkSpider(url)
            #home_spider.parse_page()
            #home_spider.save_data_to_model()
            return HttpResponseRedirect('../grade/')    #和Homework/urls.py中path('', include('home_link.urls'))绑定
    else:
        return HttpResponseRedirect('../grade/')


def house_yuce(request):
    if request.method == 'POST':
        form = Grade(request.POST)
        if form.is_valid():
            yc = int(form.cleaned_data.get('yc'))
            if is_number(yc):
                yuce[0] = yc

            return HttpResponseRedirect('/pre/')    #和Homework/urls.py中path('', include('home_link.urls'))绑定
    else:
        return HttpResponseRedirect('/pre/')

def yuce_index(request):
    form = Grade()

    if yuce[0] >= 0 and yuce[0] <= 750:
        return render(request, 'home_link/predict.html',
                      context={'form': form, 'fs': yuce[0], 'yc': yuce_dict.get(str(yuce[0]))})

    else:
        return render(request, 'home_link/predict.html',
                      context={'form': form, 'yc': -1})


'''
# 预测
def linear_model_main(X_parameters, Y_parameters, predict_value):
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    predict_outcome = regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions

def show_linear_line(X_parameters, Y_parameters):
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    plt.scatter(X_parameters, Y_parameters, color='blue')
    plt.plot(X_parameters, regr.predict(X_parameters), color='red', linewidth=4)
    plt.xticks(())
    plt.yticks(())
    #plt.show()



def yuce(request):
    if request.method == 'POST':
        form = ycForm(request.POST)
        if form.is_valid():
            predictvalue = int(form.cleaned_data.get('yc'))

            all_url = [
                'https://www.ynpxrz.com/n1456209c1599.aspx',
                'http://www.zizzs.com/c/201706/17861.html',
                'http://www.gaosan.com/gaokao/217808.html',
                'https://www.gjw.cn/GaoKaoZiXun/964809-2.html',
                'http://www.gaosan.com/gaokao/64218.html']

            X = []
            Y = []

            for i in all_url:
                grade_list = GradeInfo.objects.filter(name=i).order_by('add_date')
                flag = 1
                pm = 1  # 排名
                for j in grade_list:
                    if flag:
                        X.append(list(int(j.subsection[0:3])))
                        flag = 0
                    else:
                        X.append(list(int(j.subsection)))

                    Y.append(pm)
                    pm += int(j.sum)

            predictvalue = np.array(predictvalue).reshape(1, -1)  # 书上没有这一段，执行不了。
            # 使用array重新调整数据的形状。如果数据有单个功能或数组，则重新调整形状（-1，1）。如果数据包含单个示例，则重新调整形状（1，-1）
            result = linear_model_main(X, Y, predictvalue)
            print("截距值", result['intercept'])
            print("常数值", result['coefficient'])
            print("预测值", result['predicted_value'])
            show_linear_line(X, Y)

            return HttpResponseRedirect('/')    #和Homework/urls.py中path('', include('home_link.urls'))绑定
    else:
        return HttpResponseRedirect('/')
'''


class HomeLinkSpider(object):
    def __init__(self, url):
        self.data = list()
        self.url = url

    def parse_page(self):
        response = requests.get(self.url)
        response.encoding = 'utf-8'
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser').find_all('tr')
            info = []
            for i in soup:
                l = []
                for j in i:
                    l.append(j.string)
                if l != []:
                    l = [x.strip() for x in l if x.strip() != '']
                    # print(l)
                    info.append(l)

            for i in range(1, len(info)):
                if not is_number(info[i][0][0:1]):
                    continue

                detail = dict()
                detail['subsection'] = info[i][0]
                detail['sec_num'] = info[i][1]
                detail['sum'] = info[i][2]
                #print("{}-{}-{}".format(detail['subsection'], detail['sec_num'], detail['sum']))
                self.data.append(detail)

        else:
            print("请求失败 status:{}".format(response.status_code))

    def save_data_to_model(self):
        for item in self.data:
            new_item = GradeInfo(name=name_list[0])
            new_item.subsection = item['subsection']
            new_item.sec_num = item['sec_num']
            new_item.sum = item['sum']
            new_item.save()

