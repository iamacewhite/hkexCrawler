#coding: utf8

import sys, cookielib, urllib2
from utils import *
from bs4 import BeautifulSoup
from datetime import date, timedelta
import datetime, os
#from get_list import get_list
from multiprocessing import Pool
import multiprocessing
# import qszz

header = {
    'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
    'Accept-Language' : 'zh-CN',
    'Accept' : 'text/html, application/xhtml+xml, */*',
    'Accept-Encoding' : 'gzip, deflate'
}

def run(ctx, html, kwargs):
    url = 'http://www.hkexnews.hk/sdw/search/search_sdw_c.asp'

    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPHandler(0), urllib2.HTTPCookieProcessor(cj))
    data = GetUrl(url, header = header, opener = opener)

    bs = BeautifulSoup(data, 'html5lib', from_encoding='big5')
    form = bs.find('form', attrs = {'name' : 'mainform'})
    if form is None:
        ctx.onerror(u'找不到定位点_v2.1')
        return

    txt_today_d = form.find('input', id = 'txt_today_d')
    txt_today_m = form.find('input', id = 'txt_today_m')
    txt_today_y = form.find('input', id = 'txt_today_y')
    current_page = form.find('input', id = 'current_page')
    stock_market = form.find('input', id = 'stock_market')
    IsExist_Slt_Stock_Id = form.find('input', id = 'IsExist_Slt_Stock_Id')
    IsExist_Slt_Part_Id = form.find('input', id = 'IsExist_Slt_Part_Id')
    rdo_SelectSortBy = form.find('input', id = 'rdo_SelectSortBy')
    sessionToken = form.find('input', attrs = {'name' : 'sessionToken'})
    sel_ShareholdingDate_d = form.find('select', attrs = {'name' : 'sel_ShareholdingDate_d'})
    sel_ShareholdingDate_m = form.find('select', attrs = {'name' : 'sel_ShareholdingDate_m'})
    sel_ShareholdingDate_y = form.find('select', attrs = {'name' : 'sel_ShareholdingDate_y'})

    txt_today_d = txt_today_d['value'] if txt_today_d else ''
    txt_today_m = txt_today_m['value'] if txt_today_m else ''
    txt_today_y = txt_today_y['value'] if txt_today_y else ''
    current_page = current_page['value'] if current_page else ''
    stock_market = stock_market['value'] if stock_market else ''
    IsExist_Slt_Stock_Id = IsExist_Slt_Stock_Id['value'] if IsExist_Slt_Stock_Id else ''
    IsExist_Slt_Part_Id = IsExist_Slt_Part_Id['value'] if IsExist_Slt_Part_Id else ''
    rdo_SelectSortBy = rdo_SelectSortBy['value'] if rdo_SelectSortBy else ''
    sessionToken = sessionToken['value'] if sessionToken else ''

    sel_ShareholdingDate_d = sel_ShareholdingDate_d.find('option', selected = True) if sel_ShareholdingDate_d else ''
    sel_ShareholdingDate_m = sel_ShareholdingDate_m.find('option', selected = True) if sel_ShareholdingDate_m else ''
    sel_ShareholdingDate_y = sel_ShareholdingDate_y.find('option', selected = True) if sel_ShareholdingDate_y else ''

    sel_ShareholdingDate_d = sel_ShareholdingDate_d.string if sel_ShareholdingDate_d else ''
    sel_ShareholdingDate_m = sel_ShareholdingDate_m.string if sel_ShareholdingDate_m else ''
    sel_ShareholdingDate_y = sel_ShareholdingDate_y.string if sel_ShareholdingDate_y else ''

    if txt_today_d == '' or txt_today_m == '' or txt_today_y == '' or current_page == '' or stock_market == '' or sessionToken == '' or IsExist_Slt_Stock_Id == '' or IsExist_Slt_Part_Id == '' or rdo_SelectSortBy == '' or sel_ShareholdingDate_d == '' or sel_ShareholdingDate_m == '' or sel_ShareholdingDate_y == '':
        ctx.onerror(u'找不到定位点_v2.2: txt_today_d=%s&txt_today_m=%s&txt_today_y=%s&current_page=%s&stock_market=%s&sessionToken=%s&IsExist_Slt_Stock_Id=%s&IsExist_Slt_Part_Id=%s&rdo_SelectSortBy=%s&sel_ShareholdingDate_d=%s&sel_ShareholdingDate_m=%s&sel_ShareholdingDate_y=%s&' % (txt_today_d, txt_today_m, txt_today_y, current_page, stock_market, sessionToken, IsExist_Slt_Stock_Id, IsExist_Slt_Part_Id, rdo_SelectSortBy, sel_ShareholdingDate_d, sel_ShareholdingDate_m, sel_ShareholdingDate_y))
        return
    date = kwargs['date']
    if date.day < 10:
        sel_ShareholdingDate_d = '0' + str(date.day)
    else:
        sel_ShareholdingDate_d = str(date.day)
    sel_ShareholdingDate_m = '0' + str(date.month)
    postdata = (
        ('txt_today_d', txt_today_d),
        ('txt_today_m', txt_today_m),
        ('txt_today_y', txt_today_y),
        ('current_page', current_page),
        ('stock_market', stock_market),
        ('sessionToken', sessionToken),
        ('IsExist_Slt_Stock_Id', IsExist_Slt_Stock_Id),
        ('IsExist_Slt_Part_Id', IsExist_Slt_Part_Id),
        ('rdo_SelectSortBy', rdo_SelectSortBy),
        ('sel_ShareholdingDate_d', sel_ShareholdingDate_d),
        ('sel_ShareholdingDate_m', sel_ShareholdingDate_m),
        ('sel_ShareholdingDate_y', '2016'),
        ('txt_stock_code', kwargs['code']),
        ('txt_stock_name', ''),
        ('txt_ParticipantID', 'A00003'),
        ('txt_Participant_name', ''),
    )
    data = GetUrl(url, header = header, postdata = postdata, opener = opener)
    ret = False
    if data.find(u'沒有找到紀錄'.encode('big5')) == -1:
        # ctx.save(html, data)
        print "writing..." + html
        ret = True
    else:
        print "not found"
    with open(html, 'w') as f:
        f.write(data)
    return ret
        # qszz.run(ctx, html, kwargs)
def main(all_codes, date_list):
    try:
        for code in all_codes:
            if not os.path.exists(code):
                os.mkdir(code)
            for date in date_list:
                print "process " + str(os.getpid()) + " is adding to " + code
                if os.path.exists(code + '/' + date.strftime('%m%d%Y') + '.html'):
                    continue                    
#os.remove(code + '/' + date.strftime('%m%d%Y') + '.html')
                else:
                    run(None, code + '/' + date.strftime('%m%d%Y') + '.html', {'date' : date, 'code' : code})
                    print "process " + str(os.getpid()) + " added " + code + '/' + date.strftime('%m%d%Y') + '.html'

    except Exception as e:
        print str(e)
        return False

if __name__ == '__main__':
    #csv = get_list()
    #all_codes = csv.get_list()
    with open('new_list.csv', 'r') as f:
        content = f.readlines()
    content = [item.split(',') for item in content]
    all_codes = [item[0] for item in content]
    base = date(2014, 4, 9)
    end = date(2016, 7, 25)
    # end = date(2014, 4, 10)
    delta = end - base
    date_list = [base + timedelta(days=i) for i in range(delta.days + 1)]
    # date_list = [date(2014, 11 ,16), date(2014, 11, 17)]
    # main(['00001'], date_list)
    print('Parent process %s.' % os.getpid())
    p = Pool(multiprocessing.cpu_count())
    total = multiprocessing.cpu_count()
    for i in range(multiprocessing.cpu_count()):
        p.apply_async(main, args=(all_codes[16 * (i+8): 16 * (i+9)], date_list))
    #p.apply_async(main, args=(all_codes[326 * 7:], date_list))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
