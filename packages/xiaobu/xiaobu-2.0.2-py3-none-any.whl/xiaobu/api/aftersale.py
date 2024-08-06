from json import dumps
from typing import Optional

from xiaobu.xiaobu_erp import ErpRequest


class AftersaleErpRequest(ErpRequest):
    def __init__(self, data: dict, **kwargs):
        super().__init__(**kwargs)
        self.url = '/app/Service/aftersale/aftersale.aspx'
        self.data.update(data)
        self.method = 'POST'


# 获取售后单
def aftersale_list(query_data: Optional[list] = [], page_num: int = 1, page_size: int = 20):
    '''
    获取售后单
    :param page_num: 页数
    :param page_size:  每页条数
    :param query_data:  查询条件
    :return: 查询结果
    '''
    return AftersaleErpRequest({
        '_jt_page_size': page_size,
        "__CALLBACKID": "JTable1",
        '__CALLBACKPARAM': dumps(
            {
                "Method": "LoadDataToJSON",
                "Args": [
                    page_num,
                    dumps(query_data),
                    "{}"
                ]
            }
        ),
    }
    )
