# -*- coding: utf-8 -*-

import json
import os
import re
import sys
import time
import urllib
import execjs
import pandas as pd
import requests
from fake_useragent import UserAgent
import openpyxl

def checkNameValid(name=None):
    reg = re.compile(r'[\\/:*?"<>|\r\n]+')
    valid_name = reg.findall(name)
    if valid_name:
        for nv in valid_name:
            name = name.replace(nv, "_")
    return name

def download_reports(keys):
    # 用股票代码和时间戳创建文件夹
    type = keys[0]
    date=keys[1]
    codes = keys[2].split('|')
    timestr = str(round(time.time() * 1000))
    file_path = os.path.abspath(os.curdir)+'/BK_report/'
    if not os.path.exists(file_path):
        os.makedirs(file_path)

    base_url = 'http://dcfm.eastmoney.com/EM_MutiSvcExpandInterface/api/js/get?'

    mywb = openpyxl.Workbook()
    # empty_sheet = mywb.active
    # mywb.remove(empty_sheet)

    # 所有行业板块
    all_bk = {
               '735' : '安防设备',
                '474' : '保险',
                '546' : '玻璃陶瓷',
                '733' : '包装材料',
                '537' : '材料行业',
                '729' : '船舶制造',
                '428' : '电力行业',
                '447' : '电子信息',
                '459' : '电子元件',
                '736' : '电信运营',
                '738' : '多元金融',
                '436' : '纺织服装',
                '451' : '房地产',
                '421' : '高速公路',
                '425' : '工程建设',
                '427' : '公用事业',
                '440' : '工艺商品',
                '450' : '港口水运',
                '479' : '钢铁行业',
                '484' : '国际贸易',
                '732' : '贵金属',
                '471' : '化纤行业',
                '480' : '航天航空',
                '538' : '化工行业',
                '728' : '环保工程',
                '731' : '化肥行业',
                '422' : '交运物流',
                '429' : '交运设备',
                '456' : '家电行业',
                '545' : '机械行业',
                '739' : '金属制品',
                '485' : '旅游酒店',
                '420' : '民航机场',
                '437' : '煤炭采选',
                '476' : '木业家具',
                '433' : '农牧饲渔',
                '477' : '酿酒行业',
                '730' : '农药兽药',
                '473' : '券商信托',
                '481' : '汽车行业',
                '737' : '软件服务',
                '424' : '水泥建材',
                '438' : '食品饮料',
                '454' : '塑胶制品',
                '457' : '输配电气',
                '464' : '石油行业',
                '482' : '商业百货',
                '448' : '通讯行业',
                '486' : '文化传媒',
                '740' : '文教休闲',
                '458' : '仪器仪表',
                '465' : '医药制造',
                '475' : '银行',
                '478' : '有色金属',
                '726' : '园林工程',
                '727' : '医疗行业',
                '470' : '造纸印刷',
                '539' : '综合行业',
                '725' : '装修装饰',
                '734' : '珠宝首饰',
                '910' : '专用设备',
                '498' : 'AB股',
                '499' : 'AH股',
                '689' : '阿里概念',
                '894' : '阿兹海默',
                '566' : '滨海新区',
                '629' : '北斗导航',
                '636' : 'B股',
                '675' : '病毒防治',
                '717' : '北京冬奥',
                '812' : '贬值受益',
                '845' : '百度概念',
                '860' : '边缘计算',
                '879' : '标普概念',
                '896' : '白酒',
                '501' : '次新股',
                '506' : '创投',
                '514' : '参股券商',
                '524' : '参股期货',
                '525' : '参股银行',
                '534' : '成渝特区',
                '604' : '参股保险',
                '638' : '创业成份',
                '671' : '彩票概念',
                '679' : '超导概念',
                '700' : '充电桩',
                '703' : '超级电容',
                '742' : '创业板综',
                '811' : '超级品牌',
                '824' : '参股360',
                '859' : '超清视频',
                '862' : '超级真菌',
                '874' : '创业板壳',
                '899' : 'CRO',
                '905' : '传感器',
                '920' : '车联网',
                '950' : '草甘膦',
                '619' : '3D打印',
                '622' : '地热能',
                '634' : '大数据',
                '665' : '电商概念',
                '676' : '独家药品',
                '814' : '大飞机',
                '835' : '独角兽',
                '838' : '东北振兴',
                '853' : '电子竞技',
                '865' : '电子烟',
                '870' : '单抗概念',
                '881' : '3D玻璃',
                '901' : '3D摄像头',
                '664' : '二胎概念',
                '875' : 'ETC',
                '595' : '风能',
                '690' : '氟化工',
                '842' : '富士康',
                '867' : '富时概念',
                '878' : '分拆预期',
                '491' : '高校',
                '567' : '股权激励',
                '667' : '国家安防',
                '683' : '国企改革',
                '696' : '国产软件',
                '713' : '2025规划',
                '714' : '5G概念',
                '723' : '高送转',
                '803' : '股权转让',
                '807' : '共享经济',
                '810' : '工业4.0',
                '832' : '工业互联',
                '856' : '工业大麻',
                '868' : 'GDR概念',
                '884' : '光刻胶',
                '891' : '国产芯片',
                '904' : '广电',
                '500' : 'HS300_',
                '512' : '化工原料',
                '547' : '黄金概念',
                '577' : '核能核电',
                '601' : '海工装备',
                '623' : '海洋经济',
                '637' : '互联金融',
                '672' : '沪企改革',
                '707' : '沪股通',
                '715' : '航母概念',
                '724' : '海绵城市',
                '837' : '互联医疗',
                '854' : '华为概念',
                '908' : 'HIT电池',
                '697' : 'IPO受益',
                '897' : 'IPv6',
                '490' : '军工',
                '494' : '节能环保',
                '536' : '基金重仓',
                '552' : '机构重仓',
                '561' : '基本金属',
                '684' : '京津冀',
                '685' : '举牌概念',
                '693' : '基因测序',
                '719' : '健康中国',
                '806' : '精准医疗',
                '808' : '军民融合',
                '849' : '京东金融',
                '850' : '进口博览',
                '887' : '鸡肉概念',
                '909' : '降解塑料',
                '818' : '可燃冰',
                '820' : '壳资源',
                '990' : '快递概念',
                '574' : '锂电池',
                '580' : 'LED',
                '674' : '蓝宝石',
                '710' : '量子通信',
                '852' : '冷链物流',
                '873' : '垃圾分类',
                '906' : '流感',
                '492' : '煤化工',
                '626' : '美丽中国',
                '698' : '免疫治疗',
                '821' : 'MSCI中国',
                '857' : 'MSCI大盘',
                '858' : 'MSCI中盘',
                '890' : 'MLCC',
                '902' : 'MiniLED',
                '855' : '纳米银',
                '888' : '农业种植',
                '840' : 'OLED',
                '666' : '苹果概念',
                '721' : 'PPP模式',
                '877' : 'PCB',
                '535' : 'QFII重仓',
                '699' : '全息技术',
                '711' : '券商概念',
                '830' : '区块链',
                '864' : '氢能源',
                '872' : '青蒿素',
                '596' : '融资融券',
                '682' : '燃料电池',
                '706' : '人脑工程',
                '800' : '人工智能',
                '866' : '人造肉',
                '892' : '乳业',
                '511' : 'ST概念',
                '520' : '社保重仓',
                '548' : '生物疫苗',
                '549' : '深圳特区',
                '568' : '深成500',
                '597' : '水利建设',
                '611' : '上证50_',
                '612' : '上证180_',
                '614' : '食品安全',
                '617' : '石墨烯',
                '633' : '送转预期',
                '642' : '手游概念',
                '643' : '上海自贸',
                '669' : '生态农业',
                '705' : '上证380',
                '709' : '赛马概念',
                '743' : '深证100R',
                '804' : '深股通',
                '836' : '数字中国',
                '851' : '纾困概念',
                '861' : '数字孪生',
                '883' : '数字货币',
                '970' : '生物识别',
                '588' : '太阳能',
                '592' : '铁路基建',
                '625' : '通用航空',
                '632' : '土地流转',
                '644' : '特斯拉',
                '708' : '体育产业',
                '805' : '钛白粉',
                '841' : '体外诊断',
                '843' : '天然气',
                '863' : '透明工厂',
                '898' : '胎压监测',
                '880' : 'UWB概念',
                '885' : 'VPN',
                '509' : '网络游戏',
                '554' : '物联网',
                '655' : '网络安全',
                '704' : '无人机',
                '802' : '无人驾驶',
                '831' : '万达概念',
                '893' : '无线耳机',
                '895' : '维生素',
                '940' : '网红直播',
                '960' : '无线充电',
                '493' : '新能源',
                '519' : '稀缺资源',
                '523' : '新材料',
                '578' : '稀土永磁',
                '600' : '新三板',
                '695' : '小金属',
                '722' : '虚拟现实',
                '813' : '雄安新区',
                '825' : '新零售',
                '833' : '小米概念',
                '834' : '乡村振兴',
                '900' : '新能源车',
                '556' : '移动支付',
                '563' : '油价相关',
                '570' : '预亏预减',
                '571' : '预盈预增',
                '579' : '云计算',
                '603' : '页岩气',
                '606' : '油气设服',
                '610' : '央视50_',
                '653' : '养老概念',
                '663' : '油改概念',
                '668' : '医疗器械',
                '677' : '粤港自贸',
                '712' : '一带一路',
                '823' : '养老金',
                '847' : '影视概念',
                '889' : '医疗美容',
                '903' : '云游戏',
                '505' : '中字头',
                '528' : '转债标的',
                '581' : '智能电网',
                '594' : '长江三角',
                '615' : '中药',
                '628' : '智慧城市',
                '635' : '中超概念',
                '640' : '智能机器',
                '641' : '智能穿戴',
                '656' : '智能电视',
                '662' : '在线教育',
                '680' : '智能家居',
                '692' : '在线旅游',
                '701' : '中证500',
                '718' : '证金持股',
                '801' : '增强现实',
                '815' : '昨日涨停',
                '816' : '昨日连板',
                '817' : '昨日触板',
                '822' : '租售同权',
                '839' : '知识产权',
                '882' : '猪肉概念',
                '886' : '智慧政务',
                '907' : '转基因',
                '980' : '债转股',
                '150' : '北京板块',
                '170' : '重庆板块',
                '151' : '福建板块',
                '152' : '甘肃板块',
                '153' : '广东板块',
                '154' : '广西板块',
                '173' : '贵州板块',
                '146' : '黑龙江',
                '155' : '河北板块',
                '156' : '河南板块',
                '157' : '湖北板块',
                '158' : '湖南板块',
                '176' : '海南板块',
                '148' : '吉林板块',
                '159' : '江苏板块',
                '160' : '江西板块',
                '161' : '辽宁板块',
                '162' : '宁夏板块',
                '175' : '内蒙古',
                '163' : '青海板块',
                '145' : '上海板块',
                '164' : '山东板块',
                '165' : '陕西板块',
                '167' : '山西板块',
                '169' : '四川板块',
                '166' : '天津板块',
                '147' : '新疆板块',
                '174' : '西藏板块',
                '171' : '云南板块',
                '172' : '浙江板块'
       }
    if type == "1" :
        codes = all_bk.keys()

    current_line = 3
    print("共{}个板块，开始下载".format(len(codes)))
    all_date_type = ['y', 'jd', 'm', '10', '5', '3', '1']
    for code in codes:
        key = code
        bk_name = all_bk.setdefault(code, "未知板块")
    #for (key, value) in all_bk.items():
        #######3
        # mywb.create_sheet(bk_name)
        # mysheet = mywb[bk_name]
        mysheet = mywb.active
        mysheet["A{}".format(current_line)] = "代码"
        mysheet["B{}".format(current_line)] = "名称"
        mysheet["C{}".format(current_line)] = "股价"
        mysheet["D{}".format(current_line)] = "外资持股"
        mysheet["E{}".format(current_line)] = "占流通股比"
        mysheet["F{}".format(current_line)] = "占总股本比"
        mysheet["G{}".format(current_line)] = "年增持"
        mysheet["H{}".format(current_line)] = "季增持"
        mysheet["I{}".format(current_line)] = "月增持"
        mysheet["J{}".format(current_line)] = "10日"
        mysheet["K{}".format(current_line)] = "5日"
        mysheet["L{}".format(current_line)] = "3日"
        mysheet["M{}".format(current_line)] = "1日"
        mysheet["N{}".format(current_line)] = "行业"

        ##########

        bk_items = {}
        for index in range(len(all_date_type)):
            date_type = all_date_type[index]
            data = {
                'type': 'HSGT20_GGTJ_SUM_BK',
                'token': '894050c76af8597a853f5b408b759f5d',
                'st': 'ShareSZ_Chg_One',
                'sr': -1,
                'p': 1,
                'ps': 9999,
                #'js': '{"hits":(tc),"TotalPage":(tp),"data":(x)}',
                'filter': '(ORIGINALCODE=\''+key+'\' and DateType=\''+date_type+'\' and HdDate=\''+date+'\')',
                'rt': 52667992
            }
            #print(data)
            query_string_parameters = urllib.parse.urlencode(data)
            url = base_url + query_string_parameters
            headers = {
                'Referer':  'http://data.eastmoney.com/hsgtcg/BK0'+key+'.html',
                'User-Agent': UserAgent().random,
                'Connection': 'close',
            }
            try:
                r = requests.get(url, headers=headers)
                result = json.loads(r.text)
                for item in result:
                    code = item["SCode"]
                    if code not in bk_items:
                        bk_items[code] = {
                                            "code": item["SCode"],
                                            "name": item["SName"],
                                            "price": item["NewPrice"],
                                            "hold": item["ShareHold"],
                                            "LTZB": item["LTZB"],
                                            "ZZB": item["ZZB"]
                                            }
                    bk_items[code][date_type] = item["ShareSZ_Chg_One"]
            except Exception as e:
                print("查询'{} - {}'发生错误, 等待5秒重试".format(code , bk_items.setdefault(code, {}).setdefault("name", "未知股票")))
                try:
                    r = requests.get(url, headers=headers)
                    result = json.loads(r.text)
                    for item in result:
                        code = item["SCode"]
                        if code not in bk_items:
                            bk_items[code] = {
                                                "code": item["SCode"],
                                                "name": item["SName"],
                                                "price": item["NewPrice"],
                                                "hold": item["ShareHold"]
                                                }
                        bk_items[code][date_type] = item["ShareSZ_Chg_One"]
                except Exception as e:
                    print("查询'{} - {}'发生错误, 不再重试".format(code , bk_items.setdefault(code, {}).setdefault("name", "未知股票")))
                    pass

        for (key, value) in bk_items.items():
            current_line = current_line + 1
            mysheet["A{}".format(current_line)] = value.setdefault("code", '000000')
            mysheet["B{}".format(current_line)] = value.setdefault("name", '000000')
            mysheet["C{}".format(current_line)] = value.setdefault("price", '000000')
            mysheet["D{}".format(current_line)] = value.setdefault("hold", '000000')
            mysheet["E{}".format(current_line)] = value.setdefault("LTZB", '000000')
            mysheet["F{}".format(current_line)] = value.setdefault("ZZB", '000000')
            mysheet["G{}".format(current_line)] = value.setdefault("y", '000000')
            mysheet["H{}".format(current_line)] = value.setdefault("jd", '000000')
            mysheet["I{}".format(current_line)] = value.setdefault("m", '000000')
            mysheet["J{}".format(current_line)] = value.setdefault("10", '000000')
            mysheet["K{}".format(current_line)] = value.setdefault("5", '000000')
            mysheet["L{}".format(current_line)] = value.setdefault("3", '000000')
            mysheet["M{}".format(current_line)] = value.setdefault("1", '000000')
            mysheet["N{}".format(current_line)] = bk_name
        try:
            current_line = current_line + 5
            print("'{}'查询完毕，暂停5秒".format(bk_name))
            time.sleep(5)
        except Exception as e:
            print(value)
            pass
        #time.sleep(15)
    file_name = "{}_{}.xlsx".format(str(date), timestr)
    mywb.save(file_path+file_name)


if __name__ == "__main__":
    print('\n板块行情下载工具\n')
    while 1:
        type = input('请输入下载类型(1:所有版块，2:指定版块)：')
        date=input('请输入结束日期（格式:yyyy-mm-dd，必填，按Enter确认）：')
        if type == "2" :
            codes = input('请输入行业代码（格式:xxx、xxx、xxx[如: 735|940]，必填，按Enter确认）：')
        else:
            codes = ""
        # beginTime=input('请输入查询起始日期（格式：yyyy-mm-dd,选填，按Enter确认）：')
        # endTime=input('请输入查询结束日期（格式：yyyy-mm-dd,选填，按Enter确认）：')
        keys=[i.replace(' ','') for i in [type, date, codes]]
        download_reports(keys)
        print('板块行情数据已下载完成\n')
