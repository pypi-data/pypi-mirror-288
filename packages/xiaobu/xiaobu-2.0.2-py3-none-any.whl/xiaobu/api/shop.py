import json
from typing import Optional

from requests import Response

from xiaobu.xiaobu_erp import ErpRequest, API_ERP321_BASE_URL


class ShopErpRequest(ErpRequest):
    def __init__(self, url: str, data: dict = None, base_url=None):
        super().__init__(url=url, base_url=base_url)
        self.data = data
        self.method = 'POST'
        self.callback = callback


def callback(res: Response):
    resp_text = res.text
    resp_data = json.loads(resp_text[resp_text.find('{'):])

    if not resp_data.get('data'):
        return None
    return resp_data.get('data')


# 获取店铺信息
def get_shop_list(shop_name: Optional[str] = None, shop_type: Optional[str] = None):
    data = {
        "coid": "10174711",
        "uid": "18683738",
        "ip": "",
        "data": {
            "groupId": "",
            "enabled": 1
        },
        "page": {
            "currentPage": 1,
            "pageSize": 200
        }
    }
    if shop_name:
        data['data']['shopName'] = shop_name
    if shop_type:
        data['data']['shopType'] = shop_type
    return ShopErpRequest(data=data, url='/erp/webapi/ShopApi/ShopPage/GetShopList', base_url=API_ERP321_BASE_URL)
