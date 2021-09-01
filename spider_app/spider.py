# -*- coding = utf-8 -*-
# @Time : 2021/5/23 9:26 下午
# @File : spider_1688.py
# @Software : products
"""
1. 请在登录淘宝（https://www.taobao.com）, 京东（https://www.jd.com）和1688（https://pjjx.1688.com/）
之后获取到headers和param填入get_data_1688(), get_Data_taobao(), get_data_jd()中的header字典与param
2. 此框架添加了抓取京东评论数据的函数，需要在抓取数据动态页面函数get_jd_comment()的header，param和cookie变量与字典内容
3. 京东评价内容必须在登录之后才能查看，否则此数据正常浏览的情况下不显示在页面。数据储存在页面返回的jQuery文件中
"""

import time
import requests
import re  # 正则表达式，进行文字匹配
import urllib.request, urllib.error, urllib.parse  # 定制URL，获取网页数据
import ssl
import urllib
from lxml import etree
from .models import essencial_field
import demjson

ssl._create_default_https_context = ssl._create_unverified_context

items = essencial_field.objects.get(id=1)
jd_header = items.jd_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
jd_comment_cookie = items.jd_comment_cookie.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
jd_comment_header = items.jd_comment_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
pjjx_header = items.pjjx_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')
tb_header = items.tb_header.replace('\n', '').replace('\r', '').replace('    ', '').replace(' ', '')


def get_Data_1688(baseurl, keyword):
    datalist = []
    # print(len(datalist))
    keys = {"keywords": keyword}
    real_key = urllib.parse.urlencode(keys)
    url = baseurl + real_key
    for page in range(7):
        """
        1. 目前使用cookie方式绕过登录进行搜索内容，需要拷贝数据源的页面地址中的headers和params数据
        2. 登陆完账号之后拷贝当前页面的cURL在https://curl.trillworks.com/上转换为headers和param的字典粘贴到下方
        """
        headers = demjson.decode(pjjx_header)

        params = (
            ('start', str(page * 60)),  #
            ('pageSize', '60'),
            ('keywords', keyword.encode('utf-8')),
            # 保留以上信息添加其他信息
            ('callback', 'jQuery1830530169495744514_1629602281901'),
            ('namespace', 'AllianceSearchOfferFromSw'),
            ('widgetId', 'AllianceSearchOfferFromSw'),
            ('methodName', 'execute'),
            ('_tb_token_', '7788777b08b5e'),
            ('sortType', 'normal'),
            ('descendOrder', 'true'),
            ('_', '1629602282469'),
        )
        html = ''
        try:
            response = requests.get(url, headers=headers, params=params)
            html = response.text  # print(html) # test print
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        for a in range(0, 60):
            data = []
            # match the target by regx
            title = re.findall('"name":"(.*?)"', html)
            if a < len(title):
                if len(title) == 0:
                    data.append('')
                else:
                    data.append(title[a])

                price = re.findall('"price":(.*?),', html)
                if len(price) == 0:
                    data.append('')
                else:
                    data.append(price[a])

                supplier = re.findall('"companyName":"(.*?)"', html)
                if len(supplier) == 0:
                    data.append('')
                else:
                    data.append(supplier[a])

                sales = re.findall('"saleQuantity":(.*?),', html)
                if len(supplier) == 0:
                    data.append('')
                else:
                    data.append(sales[a])

                link = re.findall('"sourceUrl":"(.*?)"', html)
                if len(link) == 0:
                    data.append('')
                else:
                    data.append(link[a])
                datalist.append(data)
            else:
                break
        print('1688_Page %d searching' % (page + 1))
    # print(datalist) # test print
    return datalist


def get_Data_TaoBao(baseurl, keyword):
    datalist = []
    # print(len(datalist))
    keys = {"q": keyword}
    real_key = urllib.parse.urlencode(keys)
    url = baseurl + real_key
    for page in range(5):
        """
        1. 目前使用cookie方式绕过登录进行搜索内容，需要拷贝数据源的页面地址中的headers和params数据
        2. 拷贝cURL在https://curl.trillworks.com/上转换为headers和param的字典粘贴到下方
        3. 淘宝的反爬检测更加敏感，需要频繁更新cookie和header的内容，每页搜索时间间隔2秒
        """
        params = (
            ('q', keyword.encode('utf-8')),
            ('s', str(page * 44)),
            # 此两行保留，添加其他信息
            ('type', 'p'),
            ('tmhkh5', ''),
            ('from', 'sea_1_searchbutton'),
            ('catId', '100'),
            ('spm', 'a2141.241046-cn.searchbar.d_2_searchbox'),
        )
        headers = demjson.decode(tb_header)

        html = ''
        try:
            response = requests.get(url, headers=headers, params=params)
            html = response.text
            print(html) # test print
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)
        for a in range(0, 44):
            data = []
            # match the target by regx
            title = re.findall('"raw_title":"(.*?)"', html)
            if a < len(title):
                if len(title) == 0:
                    data.append("")
                else:
                    data.append(title[a])

                price = re.findall('"view_price":"(.*?)",', html)
                if len(price) == 0:
                    data.append("")
                else:
                    data.append(price[a])

                supplier = re.findall('"nick":"(.*?)"', html)
                if len(supplier) == 0:
                    data.append("")
                else:
                    data.append(supplier[a])

                location = re.findall('"item_loc":"(.*?)"', html)
                if len(supplier) == 0:
                    data.append("")
                else:
                    data.append(location[a])

                sales = re.findall('"view_sales":"(.*?)人付款"', html)
                sale = str(sales[a])
                if len(sales) == 0:
                    data.append("")
                else:
                    if sale.find('+', 0, len(sale) - 1) and (sale.find('万', 0, len(sale) - 1) == -1):
                        result = sale.strip('+')
                        data.append(int(result))
                    elif sale.find('万+', 0, len(sale) - 1):
                        result = sale.strip('万+')
                        final = int(float(result) * 10000)
                        data.append(int(final))
                    else:
                        data.append(int(result))

                link = re.findall('"comment_url":"(.*?)"', html)
                if len(link) == 0:
                    data.append("")
                else:
                    link = link[a].encode('latin-1').decode('unicode_escape')
                    data.append('https:' + link)

                datalist.append(data)
            else:
                break
        print('TaoBao_Page %d searching' % (page + 1))
        time.sleep(2)
    # print(datalist)  # test print
    return datalist


def get_data_jd(baseurl, keyword):
    datalist = []
    keys = {
        'keyword': keyword,
    }
    real_key = urllib.parse.urlencode(keys)
    # url = baseurl + real_key
    """
    1. 目前使用cookie方式绕过登录进行搜索内容，需要拷贝数据源的页面地址中的headers和params数据
    2. 登陆完账号之后拷贝当前页面的cURL在https: // curl.trillworks.com / 上转换为headers和param的字典粘贴到下方
    """
    headers = demjson.decode(jd_header)

    for i in range(7):
        url = baseurl + str(i) + '&' + real_key
        try:
            # response = urllib.request.urlopen(request)
            # html = response.read()
            # content = etree.HTML(html)
            # print(content)
            request = requests.get(url, headers=headers)
            text = request.text
            selector = etree.HTML(text)
            lis = selector.xpath('//*[@id="J_goodsList"]/ul/li')
        except urllib.error.URLError as e:
            if hasattr(e, "code"):
                print(e.code)
            if hasattr(e, "reason"):
                print(e.reason)

        for li in lis:
            data = []
            title = li.xpath('.//div[@class="p-name p-name-type-2"]/a/em/text()')
            new_title = ''
            if len(title) == 0:
                data.append("")
            else:
                if title != 0:
                    new_title = keyword.join(title)
                    new_title = new_title.replace("\n", "")
                    new_title = new_title.replace("\t", "")
                data.append(new_title)

            price = li.xpath('.//div[@class="p-price"]/strong/i/text()')[0]
            if len(price) == 0:
                data.append("")
            else:
                data.append(price)

            supplier = li.xpath('.//div[@class="p-shop"]/span/a/text()')
            if len(supplier) == 0:
                data.append("")
            else:
                data.append(supplier[0])

            link = li.xpath('.//div[@class="p-name p-name-type-2"]/a/@href')[0]
            link = "https:" + str(link)
            if len(link) == 0:
                data.append("")
            else:
                data.append(link)
            # print(data)

            comment_id = li.xpath('.//@data-sku')
            if len(comment_id) == 0:
                data.append('')
            else:
                # comment_id = get_jd_comment(comment_id[0])
                data.append(comment_id[0])

            datalist.append(data)
            # print(len(datalist))

        count = i * 30
        fix_datalist_comment(datalist, count)
        print('JD_Page %d searching' % (i + 1))
    return datalist


def get_jd_comment(comment_id):
    rate_list = []
    comment_url = 'https://club.jd.com/comment/productCommentSummaries.action?referenceIds='
    base_url = comment_url + comment_id
    cookies = demjson.decode(jd_comment_cookie)
    headers = demjson.decode(jd_comment_header)

    params = (
        ('referenceIds', comment_id),
    )
    response = requests.get(base_url, headers=headers, params=params, cookies=cookies)
    html = response.text

    good_rate = re.findall('"GoodRate":(.*?),', html)
    # print(good_rate)
    # rate_list.append()
    return good_rate


def fix_datalist_comment(datalist, count):
    string = []
    string.clear()
    for a in range(0, 30):
        if (a + count) < len(datalist):
            string.append(datalist[a + count][4])
        else:
            break

    new_string = ''
    # print(string)
    # print(len(string))
    for s in range(len(string)):
        new_string += (string[s] + ',')
    new_string = new_string.strip(',')
    # print(new_string)

    comment_list = []
    # print(get_jd_comment(new_string))
    for c in get_jd_comment(new_string):
        c = float(c) * 100
        comment_list.append(c)

    # print(comment_list)
    for b in range(0, len(comment_list)):
        datalist[b + count][4] = comment_list[b]

    return datalist
