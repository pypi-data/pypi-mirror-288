import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from requests import Response, Request

JST_HEADERS = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cache-control': 'no-cache',
    'content-type': 'application/json',
    'jst-appkey': 'web_login',
    'jst-pv': '1.0.1',
    'jst-sdkv': '1.0.0',
    'origin': 'https://www.erp321.com',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://www.erp321.com/'
}

LOGIN_JSON = {
    'data': {
        'account': '17671271393',
        'password': 'Wh1761393@'
    }
}

CO_ID = '10174711'
ERP321_BASE_URL = 'https://www.erp321.com'
API_ERP321_BASE_URL = 'https://api.erp321.com'
API_PASS_PORT_URL = API_ERP321_BASE_URL + '/erp/webapi/UserApi/WebLogin/Passport'


# 部分接口需要验证VIEWSTATE,VIEWSTATEGENERATOR,EVENTVALIDATION
# 从aspx文档中提取,缓存并记录更新时间
def get_viewstate(html):
    soup = BeautifulSoup(html, 'html.parser')
    viewstate_value = soup.find('input', {'name': '__VIEWSTATE'}).get('value')
    viewstategenerator_value = soup.find('input', {'name': '__VIEWSTATEGENERATOR'}).get('value')
    eventvalidation_value = soup.find('input', {'name': '__EVENTVALIDATION'}).get('value')
    return {'__VIEWSTATE': viewstate_value,
            '__VIEWSTATEGENERATOR': viewstategenerator_value,
            '__EVENTVALIDATION': eventvalidation_value,
            'update_time': time.time()}


# 解析返回数据
def JTable1(res: Response):
    resp_text = res.text
    resp_data = json.loads(resp_text[resp_text.find('{'):])

    if not resp_data.get('IsSuccess'):
        raise Exception(resp_data.get('Message'))
    if resp_data['ReturnValue']:
        data_ = json.loads(resp_data['ReturnValue'])['datas']
        return data_ if data_ else []
    return []


# 所有接口由该Session调用
class ErpSession(requests.Session):
    def __init__(self):
        super().__init__()
        self.headers.update(JST_HEADERS)
        self.post(API_PASS_PORT_URL, json=LOGIN_JSON)
        self.viewstate_cache = dict()

    def erp_send(self, request: Request):
        # api接口直接请求
        if request.base_url:
            request.url = urljoin(request.base_url, request.url)
            resp = self.post(request.url, json=request.data)
        else:
            # 默认域名 erp321.com
            request.url = urljoin(ERP321_BASE_URL, request.url)
            if request.method == 'POST':
                request.headers.update({'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'})
                # 默认域名接口需要更新VIEWSTATE
                if not request.base_url:
                    self.update_viewstate(request)
            prepare_request = self.prepare_request(request)
            resp = super().send(prepare_request)

        # 解析返回数据
        if request.callback:
            return request.callback(resp)
        return resp

    def update_viewstate(self, request):
        # 每24小时更新VIEWSTATE
        if request.url in self.viewstate_cache:
            if self.viewstate_cache[request.url]['update_time'] + 60 * 60 * 24 < time.time():
                request.data.update(self.viewstate_cache[request.url])
        else:
            view_resp = self.get(request.url)
            viewstate = get_viewstate(view_resp.text)
            self.viewstate_cache[request.url] = viewstate
            request.data.update(viewstate)


class ErpRequest(requests.Request):

    def __init__(self, base_url=None, **kwargs):
        super().__init__(**kwargs)
        self.base_url = base_url
        if not self.base_url:
            self.__get_default_params()
            self.callback = JTable1

    # 默认参数
    def __get_default_params(self):
        rand_params = {
            '_c': 'jst-epaas',
            'am___': 'LoadDataToJSON',
            'owner_co_id': CO_ID,
            'authorize_co_id': CO_ID
        }
        self.params = rand_params
        self.data = rand_params
