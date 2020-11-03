import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
import unicodedata

ss = list()

def house_spider():
    url = 'http://www.gaosan.com/gaokao/64218.html'    #正确  2020
    #url = 'https://www.gjw.cn/GaoKaoZiXun/964809-2.html'     #正确   2019
    #url = 'http://www.gaosan.com/gaokao/217808.html'   #正确     2018
    #url = 'http://www.zizzs.com/c/201706/17861.html'     #正确，出现多余\n已解决     2017
    #url = 'https://www.ynpxrz.com/n1456209c1599.aspx'   #前两行中文乱码    2016
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


if __name__ == '__main__':
    house_spider()
    draw()