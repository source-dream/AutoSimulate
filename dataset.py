# 数据获取模块
from config import BASE_URL
import pandas as pd

def get_datafields(sess, searchScope, dataset_id='', search='') -> pd.DataFrame:
    """
    从WorldQuant Brain的API获取满足条件的数据字段，并返回为DataFrame格式。

    args:
        sess: requests.Session, 登录成功时返回的会话对象
        searchScope: dict, 搜索范围参数
        dataset_id: str, 数据集ID
        search: str, 搜索关键字

    returns:
        pd.DataFrame: 包含所有满足条件的数据字段。
    """

    # 获取搜索范围参数
    instrument_type = searchScope['instrumentType']
    region = searchScope['region']
    delay = searchScope['delay']
    universe = searchScope['universe']

    # 根据是否提供搜索关键字设置URL模板
    if len(search) == 0:
        url = (
            f"{BASE_URL}/data-fields?" +\
            f"instrumentType={instrument_type}" +\
            f"&region={region}" +\
            f"&delay={str(delay)}" +\
            f"&universe={universe}" +\
            f"&dataset.id={dataset_id}" +\
            "&limit=50" +\
            "&offset={x}"
        )
        # 获取满足条件的总记录数
        res = sess.get(url.format(x=0))
        count = res.json()['count']
    else:
        url = (
            f"{BASE_URL}/data-fields?" +\
            f"instrumentType={instrument_type}" +\
            f"&region={region}" +\
            f"&delay={str(delay)}" +\
            f"&universe={universe}" +\
            "&limit=50" +\
            f"&search={search}" +\
            "&offset={x}"
        )
        count = 100

    # 初始化列表存储所有的数据字段
    datafields_list = []
    for x in range(0, count, 50):
        # 分批次获取数据字段
        datafields = sess.get(url.format(x=x))
        datafields_list.append(datafields.json()['results'])

    # 转换为DataFrame
    datafields_list_flat = [item for sublist in datafields_list for item in sublist]
    datafields_df = pd.DataFrame(datafields_list_flat)
    return datafields_df