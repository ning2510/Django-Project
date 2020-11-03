import requests
from bs4 import BeautifulSoup
import unicodedata

def house_spider():
    # url = 'http://www.gaosan.com/gaokao/64218.html'    #正确  2020
    # url = 'https://www.gjw.cn/GaoKaoZiXun/964809-2.html'     #正确   2019
    # url = 'http://www.gaosan.com/gaokao/217808.html'   #正确     2018
    # url = 'http://www.zizzs.com/c/201706/17861.html'     #正确，出现多余\n已解决     2017
    url = 'https://www.ynpxrz.com/n1456209c1599.aspx'  # 前两行中文乱码    2016
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

            for i in range(1, len(info)):
                if not is_number(info[i][0][0:1]):
                    continue

                detail = dict()
                detail['subsection'] = info[i][0]
                detail['sec_num'] = info[i][1]
                detail['sum'] = info[i][2]
                print("{}-{}-{}".format(detail['subsection'], detail['sec_num'], detail['sum']))
                self.data.append(detail)

        else:
            print("请求失败 status:{}".format(response.status_code))

    def save_data_to_model(self):
        for item in self.data:
            print("{}-{}-{}".format(item['subsection'], item['sec_num'], item['sum']))

#house_spider()

f = open("shuju.txt", 'r' )
new_dict = dict([i.strip().split('\t') for i in f])
f.close()

for i in new_dict:
    print("{} {}".format(i, new_dict[i]))