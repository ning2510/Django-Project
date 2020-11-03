import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
##from sklearn.metrics import mean_squared_error, r2_score

import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import unicodedata

ss = list()

def house_spider():
    all_url = [
        'https://www.ynpxrz.com/n1456209c1599.aspx',
        'http://www.zizzs.com/c/201706/17861.html',
        'http://www.gaosan.com/gaokao/217808.html',
        'https://www.gjw.cn/GaoKaoZiXun/964809-2.html',
        'http://www.gaosan.com/gaokao/64218.html']

    for url in all_url:
        home_spider = HomeLinkSpider(url)
        home_spider.parse_page()
        #home_spider.save_data_to_model()


def is_number(s):
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
                    #print(l)
                    info.append(l)

            flag = 1

            for i in range(1, len(info)):
                if not is_number(info[i][0][0:1]):
                    continue

                detail = dict()
                if flag:
                    detail['subsection'] = int(info[i][0][0:3])
                    flag = 0
                else:
                    detail['subsection'] = int(info[i][0])

                detail['sec_num'] = int(info[i][1])
                detail['sum'] = int(info[i][2])
                ss.append(detail)

        else:
            print("请求失败 status:{}".format(response.status_code))

def draw():
    sec_sum = [0] * 15
    sum = [0] * 15
    grade = ['0-50', '51-100', '101-150', '151-200', '201-250', '251-300', '301-350', '351-400', '401-450', '451-500', '501-550', '551-600', '601-650', '651-700', '701-750']
    #grade = ['50', '100', '150', '200', '250', '300', '350', '400', '450', '500', '550', '600', '650', '700', '750']

    for i in ss:
        x = i['subsection']
        y = i['sec_num']
        z = i['sum']
        if x == 0:
            x = x + 1
        id = (x - 1) // 50
        sec_sum[id] = sec_sum[id] + y
        sum[id] = max(sum[id], z)

    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 5))
    plt.title('黑龙江省2020年高考理科成绩一分一段表', fontsize='xx-large')
    plt.xlabel('分段')
    plt.xticks(rotation=45)
    plt.ylabel('总数')
    plt.plot_date(grade, sec_sum, '-', color='b', label='段内人数')
    plt.plot_date(grade, sum, '-', color='r', label='累计人数')


    plt.legend()
    plt.grid(linestyle=":")
    plt.show()


def linear_model_main(X_parameters, Y_parameters, predict_value):
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    predict_outcome=regr.predict(predict_value)
    predictions = {}
    predictions['intercept'] = regr.intercept_
    predictions['coefficient'] = regr.coef_
    predictions['predicted_value'] = predict_outcome
    return predictions

def show_linear_line(X_parameters, Y_parameters):
    regr = linear_model.LinearRegression()
    regr.fit(X_parameters, Y_parameters)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.figure(figsize=(10, 5))
    plt.title('黑龙江省高考理科成绩预测', fontsize='xx-large')
    plt.scatter(X_parameters, Y_parameters, color='blue', marker=".")
    plt.plot(X_parameters, regr.predict(X_parameters), color='red', linewidth=1)
    plt.xlabel('分数')
    plt.ylabel('排名')
    plt.xticks(())
    plt.yticks(())
    plt.show()

def yuce():
    X = list()
    Y = list()

    num = 1
    for i in ss:
        a, b, c = i['subsection'], i['sec_num'], i['sum']
        if num > c:
            num = 1
        X.append([a])
        Y.append(num)
        num = c + 1


    predictvalue = 0
    predictvalue = np.array(predictvalue).reshape(1, -1)  # 书上没有这一段，执行不了。
    # 使用array重新调整数据的形状。如果数据有单个功能或数组，则重新调整形状（-1，1）。如果数据包含单个示例，则重新调整形状（1，-1）
    result = linear_model_main(X, Y, predictvalue)
    # print("截距值", result['intercept'])
    # print("常数值", result['coefficient'])

    ans = int(result['predicted_value'])
    if ans <= 0:
        ans = 1
    print("预测值", ans)
    show_linear_line(X, Y)


    '''
    pp = list()
    
    for predictvalue in range(650, 751):
        predictvalue = np.array(predictvalue).reshape(1, -1)#书上没有这一段，执行不了。
        #使用array重新调整数据的形状。如果数据有单个功能或数组，则重新调整形状（-1，1）。如果数据包含单个示例，则重新调整形状（1，-1）
        result=linear_model_main(X, Y, predictvalue)
        #print("截距值", result['intercept'])
        #print("常数值", result['coefficient'])

        ans = int(result['predicted_value'])
        if ans <= 0:
            ans = 1
        #print("预测值", ans)
        pp.append(ans)
        show_linear_line(X, Y)

    for i in pp:
        print(i)
    '''

if __name__ == '__main__':
    house_spider()      # 爬虫
    #draw()             # 画图

    #for i in ss:
    #    print("{} {} {}".format(i['subsection'], i['sec_num'], i['sum']))

    yuce()              # 预测
