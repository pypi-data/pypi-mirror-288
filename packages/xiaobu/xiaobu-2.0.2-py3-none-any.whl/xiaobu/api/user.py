from xiaobu.xiaobu_erp import ErpRequest, API_ERP321_BASE_URL

LOGIN_JSON = {
    'data': {
        'account': '17671271393',
        'password': 'Wh1761393@'
    }
}


class UserErpRequest(ErpRequest):
    def __init__(self, url: str, data: dict = None, base_url=None):
        super().__init__(url=url, base_url=base_url)
        self.data = data
        self.method = 'POST'


# 获取售后单
def pass_port():
    return UserErpRequest(data=LOGIN_JSON, url='/erp/webapi/UserApi/WebLogin/Passport', base_url=API_ERP321_BASE_URL)
