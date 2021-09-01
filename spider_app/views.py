import codecs

from django.http import HttpResponse
from django.shortcuts import render, HttpResponseRedirect
import csv
from .models import data_1688, data_jd, data_taobao, essencial_field, users
from .spider import get_data_jd, get_Data_1688, get_Data_TaoBao, get_jd_comment

"""
1. 请在登录淘宝（https://www.taobao.com）, 京东（https://www.jd.com）和1688（https://pjjx.1688.com/）
之后获取到headers和param填入get_data_1688(), get_Data_taobao(), get_data_jd()中的header字典与param
2. 此框架添加了抓取京东评论数据的函数，需要在抓取数据动态页面函数get_jd_comment()的header，param和cookie变量与字典内容
3. 京东评价内容必须在登录之后才能查看，否则此数据正常浏览的情况下不显示在页面。数据储存在页面返回的jQuery文件中
"""


# Create your views here.
def hello(request):
    return render(request, 'hello.html')


def login(request):
    if 'login' in request.POST:
        check_username = request.POST.get('username')
        check_password = request.POST.get('password')
        result = users.objects.filter(username=check_username, password=check_password)
        if not result:
            return render(request, 'login.html', {'msg': '请输入正确的用户名和密码'})
        else:
            return HttpResponseRedirect('/searching')
    return render(request, 'login.html')


def register(request):
    if 'register' in request.POST:
        new_username = request.POST.get('username')
        new_password = request.POST.get('password')
        pairs = users.objects.filter(username=new_username, password=new_password)
        if pairs:
            return render(request, 'register.html', {'msg': '用户已存在'})
        else:
            new_user = users.objects.create(username=new_username, password=new_password)
            new_user.save()
            return render(request, 'login.html', {'msg': '注册成功！'})
    return render(request, 'register.html')


def addFields(request):
    if 'update_fields' in request.POST:
        line = essencial_field.objects.filter()
        jd_headers = request.POST.get('jd_header')
        jd_comment_header = request.POST.get('jd_comment_header')
        jd_comment_cookie = request.POST.get('jd_comment_cookie')
        tb_headers = request.POST.get('tb_header')
        pjjx_headers = request.POST.get('1688_header')

        if line.exists():
            item = essencial_field.objects.get(id=1)
            item.jd_header = jd_headers
            item.jd_comment_header = jd_comment_header
            item.jd_comment_cookie = jd_comment_cookie
            item.tb_header = tb_headers
            item.pjjx_header = pjjx_headers
            item.save()
            return render(request, 'essential_fields.html', {'result': item})
        else:

            add_lines = essencial_field(jd_header=jd_headers, jd_comment_header=jd_comment_header,
                                        jd_comment_cookie=jd_comment_cookie, tb_header=tb_headers,
                                        pjjx_header=pjjx_headers)
            add_lines.save()

            return render(request, 'essential_fields.html', {'result': 'Saved'})
    else:
        lines = essencial_field.objects.get(id=1)
        return render(request, 'essential_fields.html', {'result': lines})


def searching(request):
    if 'send_key' in request.POST:
        key = request.POST.get('get_key')
        print(key)
        if key:
            data_jd.objects.all().delete()
            data_1688.objects.all().delete()
            data_taobao.objects.all().delete()
            baseurl_1688 = 'https://widget.1688.com/front/getJsonComponent.json?'
            baseurl_TaoBao = 'https://s.taobao.com/search?'
            baseurl_jd = 'https://search.jd.com/Search?page='

            datalist_jd = get_data_jd(baseurl_jd, key)
            # print(datalist_jd)
            # get comment_id from the last column of datalist_jd, column name is comment_id
            datalist_1688 = get_Data_1688(baseurl_1688, key)
            datalist_taobao = get_Data_TaoBao(baseurl_TaoBao, key)

            for item in datalist_jd:
                add_line_jd = data_jd(item=item[0], price=item[1], supplier=item[2], link=item[3], comment_id=0,
                                      rate=item[4])
                add_line_jd.save()

            for item in datalist_1688:
                add_line_1688 = data_1688(item=item[0], price=item[1], supplier=item[2], sale=item[3], link=item[4])
                add_line_1688.save()

            for item in datalist_taobao:
                add_line_taobao = data_taobao(item=item[0], price=item[1], supplier=item[2], location=item[3],
                                              sale=item[4], link=item[5])
                add_line_taobao.save()

            items_jd = data_jd.objects.order_by('-rate')[:10]
            items_1688 = data_1688.objects.order_by('-sale')[:10]
            items_tb = data_taobao.objects.order_by('-sale')[:10]

            datalist = {
                'received_key': key,
                'datalist_jd': items_jd,
                'datalist_1688': items_1688,
                'datalist_tb': items_tb,
            }
            return render(request, "index.html", datalist)
        else:
            data_jd.objects.all().delete()
            data_1688.objects.all().delete()
            data_taobao.objects.all().delete()
            return render(request, "index.html", {'received_key': '请输入搜索内容'})

    elif 'jd_csv_out' in request.POST:
        result_jd = data_jd.objects.filter()
        if result_jd.exists():
            response = HttpResponse(content_type='text/csv')
            response.write(codecs.BOM_UTF8)
            # 表名
            response['Content-Disposition'] = 'attachment; filename="save_jd.csv"'
            writer = csv.writer(response)
            # 表头
            writer.writerow(['ID', '商品', '好评率%', '价格（元）', '供应商', '链接'])
            # 表数据
            items = data_jd.objects.all().values_list('id', 'item', 'rate', 'price', 'supplier', 'link')
            for item in items:
                writer.writerow(item)
            print('save_jd_Done')
            return response
        else:
            return render(request, 'index.html', {'received_key': 'jd无数据导出'})

    elif 'tb_csv_out' in request.POST:
        result_tb = data_taobao.objects.filter()
        if result_tb.exists():
            response = HttpResponse(content_type='text/csv')
            response.write(codecs.BOM_UTF8)
            # 表名
            response['Content-Disposition'] = 'attachment; filename="save_taobao.csv"'
            writer = csv.writer(response)
            # 表头
            writer.writerow(['ID', '商品名', '价格(元)', '供应商', '所在地', '销售量', '链接'])
            # 表数据
            items = data_taobao.objects.all().values_list('id', 'item', 'price', 'supplier', 'location', 'sale', 'link')
            for item in items:
                writer.writerow(item)
            print('save_tb_Done')
            return response
        else:
            return render(request, 'index.html', {'received_key': 'tb无数据导出'})

    elif '1688_csv_out' in request.POST:
        result_1688 = data_1688.objects.filter()
        if result_1688.exists():
            response = HttpResponse(content_type='text/csv')
            response.write(codecs.BOM_UTF8)
            # 表名
            response['Content-Disposition'] = 'attachment; filename="save_1688.csv"'
            writer = csv.writer(response)
            # 表头
            writer.writerow(['ID', '商品名', '价格(元)', '供应商', '月销售量', '链接'])
            # 表数据
            items = data_1688.objects.all().values_list('id', 'item', 'price', 'supplier', 'sale', 'link')
            for item in items:
                writer.writerow(item)
            print('save_1688_Done')
            return response
        else:
            return render(request, 'index.html', {'received_key': '1688无数据导出'})

    else:
        return render(request, "index.html", {'received_key': 'None'})
