'''
爬取上证综合指数(000001)年季度历史交易数据
主站：http://vip.stock.finance.sina.com.cn/corp/go.php/vMS_MarketHistory/stockid/000001/type/S.phtml
存在问题：没有robots.txt, 然而太快会被封IP
解决方案：代理IP,来源：http://cn-proxy.com/
待解决：之前写过爬取上面网站的代理IP的程序，回头把它和这个合起来
'''

import time
import csv
import requests
from bs4 import BeautifulSoup


# 获取所有数据
def get_all_data(headers, proxies=None):
    # 创建文件，用来存储数据
    file = open('stock_data.csv', 'a')
    csv_file = csv.writer(file)
    csv_file.writerow(['date', 'open', 'highest', 'close', 'lowest', 'trade_times', 'trade_money'])
    # 开始爬取
    page_urls = get_page_urls()
    for page_url in page_urls:
        try:
            time.sleep(0.5)
            page_data = requests.get(page_url, headers=headers)
            page_data.encoding = 'gbk'
            page_obj = BeautifulSoup(page_data.content, 'lxml')
            item_objs = get_page_data(page_obj)
            for item_obj in item_objs:
                get_item_data(item_obj, csv_file)
        except Exception as e:
            print(page_url)
            print(e)
    file.close()


def get_page_urls():
    page_urls = ["http://vip.stock.finance.sina.com.cn/corp/go.php/vMS" \
                 "_MarketHistory/stockid/000001/type/S.phtml?year=" + str(year) + "&jidu=" + str(season)
                 for year in range(1991, 2015) for season in range(1, 5)]
    page_urls.extend("http://vip.stock.finance.sina.com.cn/corp/go.php/vM"
                     "S_MarketHistory/stockid/000001/type/S.phtml?year=1990&jidu=4")
    return page_urls


def get_page_data(page_obj):
    page_data = page_obj.find('table', {'id': 'FundHoldSharesTable'}).findAll('tr')[2:]
    return page_data[::-1]


def get_item_data(item_obj, csv_file):
    try:
        datas = item_obj.findAll('td')
        date = datas[0].get_text().strip()
        open = datas[1].get_text()
        highest = datas[2].get_text()
        close = datas[3].get_text()
        lowest = datas[4].get_text()
        trade_times = datas[5].get_text()
        trade_money = datas[6].get_text()
        item_data = [date, open, highest, close, lowest, trade_times, trade_money]
        csv_file.writerow(item_data)
        print(item_data)
        return item_data
    except Exception as e:
        print(e)


if __name__ == '__main__':
    headers = {
        'User - Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, '
                        'like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        'Upgrade-Insecure-Requests': '1',
        'Host': 'vip.stock.finance.sina.com.cn'}

    get_all_data(headers)
