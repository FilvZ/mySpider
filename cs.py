import requests
import re
import pandas as pd
url = 'http://pss-system.cnipa.gov.cn/sipopublicsearch/patentsearch/showSearchResult-executeSearchByHistoryRegister.shtml'
data=dict()

def  get_page_html(html,page):
    data = {
        'accept': 'application/json, text/javascript, */*; q=0.01',
        # 'Cookie': 'WEE_SID=ogN95dPJvFxMdQuL4hrmexuY5Pogb8MXefIK8Otj-V786JGbYxSL!-1835415286!1724404552!1561185342409; IS_LOGIN=true; JSESSIONID=ogN95dPJvFxMdQuL4hrmexuY5Pogb8MXefIK8Otj-V786JGbYxSL!-1835415286!1724404552',
        'Cookie': 'IS_LOGIN=true; WEE_SID=s3J_0hwDVa5f2IkLk5nqtPm7HfLPhQoDhFukbl9GeDG38BNgRyiv!-1661052777!248412311!1561217604611; JSESSIONID=s3J_0hwDVa5f2IkLk5nqtPm7HfLPhQoDhFukbl9GeDG38BNgRyiv!-1661052777!248412311',
        #  'WEE_SID=IX1-0Df34IX5TR5ygkMT2BhBvRSne6spA40ZlkaS-nsvmStXohTj!-1835415286!1724404552!1561200703479; IS_LOGIN=true; JSESSIONID=IX1-0Df34IX5TR5ygkMT2BhBvRSne6spA40ZlkaS-nsvmStXohTj!-1835415286!1724404552',
        # 'Cookie': 'WEE_SID=0dJ_zjo8JHOmYUliMgrXeCggxpxjRWM6RmSGF0CcYyoLVrICtKYT!248412311!-319482382!1561217350204; IS_LOGIN=true; JSESSIONID=0dJ_zjo8JHOmYUliMgrXeCggxpxjRWM6RmSGF0CcYyoLVrICtKYT!248412311!-319482382',
        # 'user-agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
        'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'X-Requested-With': 'XMLHttpRequest'
    }
    fdata = {
        'resultPagination.limit': 12,
        'resultPagination.start': page,
        'searchCondition.executableSearchExp': "VDB:(((APD='20180101' to '20181231' AND (ABVIEW='旅游' OR ABVIEW='旅行' OR ABVIEW='旅行社' OR ABVIEW='景区' OR ABVIEW='景点' OR ABVIEW='酒店' OR ABVIEW='游客')) AND (CC='HK' OR CC='MO' OR CC='TW' OR ((DOC_TYPE='I' OR DOC_TYPE='U' OR DOC_TYPE='D') AND CC='CN'))))",
        'searchCondition.searchExp': '(申请日=20180101:20181231 AND 摘要=(旅游 旅行 旅行社 景区 景点 酒店 游客)) AND 公开国家/地区/组织=(HK OR MO OR TW OR (发明类型=("I" OR "U" OR "D") AND 公开国家/地区/组织=(CN)))',
        'searchCondition.ssId': 'a17a71baccf840f998f356e6057eb0e9',
        'searchCondition.searchType': 'Sino_foreign',
        'wee.bizlog.modulelevel': '0200505',
    }
    response = requests.post(html, headers=data,data=fdata)
    if response.status_code == 200:
        return response
    else:
        return "出现问题,错误代码"
def get_page_json(html):
    global data
    datas = html.json()
    dto = datas['searchResultDTO']
    record = dto['searchResultRecord']
    for o in record:
        # TIVIEW    专利名称
        # AP        申请号
        # APD       申请日
        # PN        公开（公告）号
        # PD        公开（公告）日
        # ICST      IPC分类号
        # PAVIEW    申请（专利权）人申
        # INVIEW    发明人
        # AA        申请人地址
        # ABVIEW    摘要

        TIVIEW = repls(o['fieldMap']['TIVIEW'])
        AP = repls(o['fieldMap']['AP'])
        APD = repls(o['fieldMap']['APD'])
        PN = repls(o['fieldMap']['PN'])
        PD = repls(o['fieldMap']['PD'])
        ICST = repls(o['fieldMap']['ICST'])
        PAVIEW = repls(o['fieldMap']['PAVIEW'])
        INVIEW = repls(o['fieldMap']['INVIEW'])
        AA = repls(o['fieldMap']['AA'])

        data['专利名称'].append(TIVIEW)
        data['申请号'].append(AP)
        data['申请日'].append(APD)
        data['公开（公告）号'].append(PN)
        data['公开（公告）日'].append(PD)
        data['IPC分类号'].append(ICST)
        data['申请（专利权）人申'].append(PAVIEW)
        data['发明人'].append(INVIEW)
        data['申请人地址'].append(AA)
        mlist = o['textList']
        for a in mlist:
            ABVIEW = repls(a['itemValue'])
        # print(TIVIEW,AP,APD,PN,ICST,PAVIEW,INVIEW,AA)
        # print(TIVIEW)
        data['摘要'].append(ABVIEW)
def ini():
    global data
    data['专利名称'] = []
    data['申请号'] = []
    data['申请日'] = []
    data['公开（公告）号'] = []
    data['公开（公告）日'] = []
    data['IPC分类号'] = []
    data['申请（专利权）人申'] = []
    data['发明人'] = []
    data['申请人地址'] = []
    data['摘要'] = []
def main():
    ini()
    try:
        for i in range(168):
        # for i in range(107,109):
            print('第',i,'页')
            # try
            html = get_page_html(url,i*12)
            get_page_json(html)
    except Exception as e:
        print(e)
    finally:
        df = pd.DataFrame(data)
        df.to_excel("c:\demo1.xlsx", sheet_name="数据", index=False, header=True)
def repls(the_str):
    p = re.compile(r'(?P<star>(.*))(<FONT>)(?P<center>(.*))(</FONT>)(?P<end>(.*))',re.I)
    # the_str='一种户外运动<FONT>旅行</FONT>水杯'
    def f2(m2):
        d = m2.groupdict()
        return d['star'] + d['center'] + d['end']
    return p.sub(f2, the_str)

if __name__=="__main__":
    main()