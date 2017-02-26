# coding=UTF-8
import requests
s = requests.Session()
seen=set()
cookie = 'abtest=0; _fecdn_=1; __uuid=1487091016830.58; __uv_seq=78; Hm_lvt_a2647413544f5a04f00da7eee0d5e200=1487091017,1487135746; _uuid=3D88258AFFA8440B23F0FB0C953A7D93; user_kind=1; verifycode=5618693be9854188b80af44fe801dbf8; __tlog=1487135746210.44|00000000|00000000|s_o_001|s_o_001; __session_seq=28; Hm_lpvt_a2647413544f5a04f00da7eee0d5e200=1487140770; _mscid=00000000; login_temp=islogin; __nnn_bad_na_=1e5868e83e80be55; _e_ld_auth_=df42087bf3a75fec; JSESSIONID=04BDABC03E01EE51E0727FDFE89283A5; user_name=%E9%AB%98; user_id=ed581f3c867bb3136f22e79200b1344f; lt_auth=u%2BkLOXUNyVv%2BtnfQ2Gpd5PwZi4quVj6dpX9YhRoF1dW5CPG24P3nRQOBprUFxBIhlU90IcULNbj5%0D%0ANOz8yntC70ESwG6miZywtOW71XweR%2BVcdfWmhKr4kpiDFJl0nCoKmXM3oHlPlE3z5RN0YdHrwVo%3D%0D%0A; em_username=9358939482b2696581249; em_token=YWMtxgK7_PLVEeaopKsXR-LFek8TxtBqMxHkgus5YKfC9XHF_rog8tUR5rXJETnsRxGNAwMAAAFaPYje3ABPGgAt5WEnNdF3yWqLi6DHaZ5hU6BdM5QmeEkH5SfLzIfWKA; b-beta2-config=%7B%22hasPhoneNum%22%3A%221%22%2C%22ecreate_time%22%3A%2220170215%22%2C%22v%22%3A%220%22%2C%22d%22%3A-1%2C%22e%22%3A9111484%2C%22ejm%22%3A%221%22%2C%22entry%22%3A%220%22%2C%22p%22%3A%222%22%2C%22n%22%3A%22%E9%AB%98%22%2C%22audit%22%3A%222%22%2C%22ecomp_id%22%3A9111484%2C%22jz%22%3A%220%22%2C%22version%22%3A%220%22%7D'
cookie_dict = dict((line.split('=') for line in cookie.strip().split(";")))
url="https://lpt.liepin.com/soresume/so/"
header={
    'Host':'lpt.liepin.com',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:51.0) Gecko/20100101 Firefox/51.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate, br',
    'Referer': 'https://lpt.liepin.com/soresume/showcondition/',
    'Connection': 'keep-alive'
}
data={
    'filterDownload':'1',
    'searchLevel':'0',
    'contains_wantdq':'1',
    'age':'18,22',
    'sex':'女',
    'pageSize':'300',
    'searchKey':'148714537066035686842',
    #'filterKey':'148714537066035686842',
    'degrade':'false',
    'curPage':'1',
    'pn':'15'

}
s.headers.update(header)
s.cookies.update(cookie_dict)
'''
while True:
    r = requests.post(url=url,data=data,headers=header,cookies=cookie_dict, allow_redirects=False)
    loc = r.headers['location']
    if loc in seen: break
    seen.add(loc)
    print loc
'''

r=s.post(url,data)
print r.text