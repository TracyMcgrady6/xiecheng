import pandas as pd
from tools import *
import numpy as np

PRODUCT_QUANTITY = '/Users/t-mac/desktop/xiecheng/ctrip14/product_quantity.txt'
PRODUCT_INFO = '/Users/t-mac/desktop/xiecheng/ctrip14/product_info.txt'
# TRAIN = '/Users/t-mac/desktop/xiecheng/0409/train.csv'
DATE = date_range('2014-07', '2015-11')

# 读取产品信息
product_info = pd.read_csv(PRODUCT_INFO)
product_info = product_info.rename(columns={'﻿product_id': 'product_id'})
product_info = product_info.drop('railway', axis=1)
product_info = product_info.drop('airport', axis=1)
product_info = product_info.drop('citycenter', axis=1)
product_info = product_info.drop('railway2', axis=1)
product_info = product_info.drop('airport2', axis=1)
product_info = product_info.drop('citycenter2', axis=1)
product_info = product_info.drop('startdate', axis=1)
product_info = product_info.drop('upgradedate', axis=1)
product_info = product_info.drop('cooperatedate', axis=1)

# group_location = product_info.groupby(['district_id1', 'district_id2', 'district_id3'])
# group_location_dict = dict(list(group_location))
# location = {g: 'location_' + str(i) for g, i in zip(group_location_dict, range(1, len(group_location) + 1))}
# columns_list = list(product_info.columns)
# for j in range(1, len(group_location) + 1):
#     product_info['location' + str(j)] = 0

product_info['avg_price'] = 0
product_info['purchase_rate'] = 0
product_info['avg_month_quantity'] = 0
product_info['avg_month_order'] = 0

# product_info = pd.DataFrame(product_info, columns=columns_list)

product_info = product_info.fillna(0)
product_info.to_csv('/Users/t-mac/desktop/xiecheng/0424/info.csv', index=False)
product_info = pd.read_csv('/Users/t-mac/desktop/xiecheng/0424/info.csv')
# product_info = product_info.drop('district_id1', axis=1)
# product_info = product_info.drop('district_id2', axis=1)
# product_info = product_info.drop('district_id3', axis=1)
product_info = product_info.drop('district_id4', axis=1)
# product_info = product_info.drop('lat', axis=1)
# product_info = product_info.drop('lon', axis=1)
# product_info = product_info.drop('voters', axis=1)
# product_info = product_info.drop('maxstock', axis=1)

# 处理产品销售量
product_quantity = pd.read_csv(PRODUCT_QUANTITY)
product_quantity = product_quantity.rename(columns={'﻿product_id': 'product_id'})
product_quantity['product_date'] = product_quantity['product_date'].str[:7]

# 分组聚类
group = product_quantity.groupby(['product_id', 'product_date'])
group_dict = dict(list(group))


# 获得有成交记录信息的id
def get_information_quantity():
    quan_id = [i for i in range(1, 4001) if i in product_quantity['product_id'].values]
    return quan_id


have_quantity_id = get_information_quantity()
same_id_data = pd.read_csv('/Users/t-mac/desktop/xiecheng/ctrip14/same_id_1.csv')
same_id_dict = {}
for k, v in zip(same_id_data['no_quantity_id'], same_id_data['same_id']):
    same_id_dict[k] = v

# 计算每个产品每个月销量
quantity = product_quantity['ciiquantity'].groupby(
    [product_quantity['product_id'], product_quantity['product_date']]).sum()
# 按照id分组
quantity_id = product_quantity.groupby(['product_id'])
group_id = dict(list(quantity_id))
# 商品特征工程
for i in product_info.index:

    if product_info.loc[i, 'product_id'] not in have_quantity_id:
        # print(product_info.loc[i, 'product_id'], '没有销售记录')
        product_id = same_id_dict.get(product_info.loc[i, 'product_id'])
        i = product_id - 1
        # print(i)
    # # 处理地区哑变量
    # product_info.loc[i, location.get(
    #     (product_info.loc[i, 'district_id1'], product_info.loc[i, 'district_id2'],
    #      product_info.loc[i, 'district_id3']))] = 1
    # 处理商品每个月平均销量
    product_info.loc[i, 'avg_month_quantity'] = int(
        group_id[product_info.loc[i, 'product_id']]['ciiquantity'].mean() * 30)
    # 处理商品每个月平均预定量
    product_info.loc[i, 'avg_month_order'] = int(
        group_id[product_info.loc[i, 'product_id']]['ordquantity'].mean() * 30)
    # 处理商品平均价格
    # print(np.array([i for i in group[product_info.loc[i, 'product_id']]['price'] if i != -1]).mean())
    prict_list = [i for i in group_id[product_info.loc[i, 'product_id']]['price'] if i != -1]
    if len(prict_list) != 0:
        product_info.loc[i, 'avg_price'] = int(
            np.array(prict_list).mean())
    else:
        product_info.loc[i, 'avg_price'] = 0
    # 处理商品购买率
    if group_id[product_info.loc[i, 'product_id']]['ordquantity'].mean() != 0:
        product_info.loc[i, 'purchase_rate'] = float(product_info.loc[i, 'avg_month_quantity'] /
                                                     product_info.loc[i, 'avg_month_order'])


def columns_list():
    col_list = ['ciiquantity']
    col_list.extend([str('before') + str(k) for k in range(1, 7)])
    col_list.extend(['avg_by' + str(gap) + '_' + str(i) for gap in range(2, 7) for i in range(1, 8 - gap)])
    col_list.extend(['count_holiday', 'kind_of_holiday_0', 'kind_of_holiday_1', 'kind_of_holiday_2'])

    return col_list


# 最后的Train
ciiquantity = pd.DataFrame(quantity, columns=columns_list())
ciiquantity = ciiquantity.fillna(-1)

# ciiquantity = ciiquantity[:100]
for product_id, date in ciiquantity.index:
    print('id:', product_id, date)
    if date in DATE:
        sliding_window = date_range(move_month(date, -6), date)
        # 处理预定量，销售量滑动窗口
        quantity_list_nonull = [
            sum(group_dict[product_id, month_1]['ciiquantity']) for month_1 in sliding_window[:-1] if
            (product_id, month_1) in ciiquantity.index]
        if len(quantity_list_nonull) == 0:
            avg = 0
        else:
            avg = int(np.array(quantity_list_nonull).mean())
        quantity_list = [
            sum(group_dict[product_id, month_1]['ciiquantity']) if (product_id, month_1) in ciiquantity.index else avg
            for month_1 in sliding_window[:-1]]
        quantity_list.reverse()

        # 处理时间均线
        for i in range(0, 5):
            ciiquantity.loc[(product_id, date), 'avg_by2_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1]) / 2)
        for i in range(0, 4):
            ciiquantity.loc[(product_id, date), 'avg_by3_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1] + quantity_list[i + 2]) / 3)
        for i in range(0, 3):
            ciiquantity.loc[(product_id, date), 'avg_by4_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1] + quantity_list[i + 2] + quantity_list[i + 3]) / 4)
        for i in range(0, 2):
            ciiquantity.loc[(product_id, date), 'avg_by5_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1] + quantity_list[i + 2] + quantity_list[i + 3] + quantity_list[
                    i + 4]) / 5)
        ciiquantity.loc[(product_id, date), 'avg_by6_1'] = int(np.array(quantity_list).mean())
        # 处理销售量滑动窗口
        for month_1, i in zip(sliding_window[:-1], range(6, 0, -1)):
            temp_quantity = np.array([j for j in quantity_list[:i] if j != -1])
            if (product_id, month_1) in ciiquantity.index:
                ciiquantity.loc[(product_id, date), 'before' + str(i)] = sum(group_dict[product_id, month_1][
                                                                                 'ciiquantity'])
            else:  # 处理缺失情况
                if len([j for j in quantity_list[:i] if j != -1]) == 0:
                    ciiquantity.loc[(product_id, date), 'before' + str(i)] = 0
                else:
                    ciiquantity.loc[(product_id, date), 'before' + str(i)] = int(temp_quantity.mean())
        # 判断ciiquantity是否是0
        if ciiquantity.loc[(product_id, date), 'ciiquantity'] == 0:
            temp_quantity2 = np.array([j for j in quantity_list if j != -1])
            if len([j for j in quantity_list if j != -1]) != 0:
                ciiquantity.loc[(product_id, date), 'ciiquantity'] = int(temp_quantity2.mean())
            else:
                ciiquantity.loc[(product_id, date), 'ciiquantity'] = 0
        # 处理放假天数
        ciiquantity.loc[(product_id, date), 'count_holiday'] = weekandholiday.get(date)
        # 处理长短假期
        if kindofholiday.get(date) == 0:
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_0'] = 1
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_1'] = 0
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_2'] = 0
        elif kindofholiday.get(date) == 1:
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_0'] = 0
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_1'] = 1
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_2'] = 0
        else:
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_0'] = 0
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_1'] = 0
            ciiquantity.loc[(product_id, date), 'kind_of_holiday_2'] = 1
    print('---------')
ciiquantity.to_csv('/Users/t-mac/desktop/xiecheng/0424/train_temp.csv')
temp_csv = pd.read_csv('/Users/t-mac/desktop/xiecheng/0424/train_temp.csv')

temp_csv = temp_csv[temp_csv['product_date'].isin(DATE)]
# 删除-1向量
# delete = list(set(list(temp_csv['before1'].values)))
# delete.remove(-1)
# temp_csv = temp_csv[temp_csv['before1'].isin(delete)]

# temp_csv.to_csv(TRAIN)
# temp_ciiquantity = pd.read_csv(TRAIN)

result = pd.merge(temp_csv, product_info, on='product_id')

result.to_csv('/Users/t-mac/desktop/xiecheng/0424/train.csv', index=False)
