from Model import *
from tools import *

result = pd.read_csv('/Users/t-mac/desktop/xiecheng/0424/train.csv')

X, y = result.iloc[:, 3:], result.iloc[:, 2]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=33)

# model = extratrees(X_train, y_train, X_test, y_test)
model = xgboostmodel2(X_train, y_train, X_test, y_test)
# randomforest(X_train, y_train, X_test, y_test)

predeict_result = pd.read_csv('/Users/t-mac/desktop/xiecheng/0424/test.csv')
final_data = pd.read_csv('/Users/t-mac/desktop/xiecheng/ctrip14/example.txt')

for pro_date in date_range('2015-12', '2017-01'):
    print(pro_date)
    data = predeict_result[predeict_result['product_month'] == pro_date]
    predect_x = data.iloc[:, 3:]
    model_predict = model.predict(predect_x)
    # 将预测好的写入到预测结果中
    for ind, p in zip(data.index, model_predict):
        final_data.loc[ind, 'ciiquantity_month'] = int(p)
        predeict_result.loc[ind, 'ciiquantity_month'] = int(p)

    # 将预测好的写入到test中
    for temp_date, offset in zip(date_range(move_month(pro_date, 1), move_month(pro_date, 6)), range(1, 7)):
        data_offset = predeict_result[predeict_result['product_month'] == temp_date]
        for ind, p in zip(data_offset.index, model_predict):
            predeict_result.loc[ind, 'before' + str(offset)] = int(p)

    next_month = move_month(pro_date, 1)
    data_next = predeict_result[predeict_result['product_month'] == next_month]
    # 预测完毕，重新计算下个月时间均线
    for temp_ind in data_next.index:
        quantity_list_nonull = [predeict_result.loc[temp_ind, 'before' + str(i)] for i in range(1, 7) if
                                predeict_result.loc[temp_ind, 'before' + str(i)] != -1]
        if len(quantity_list_nonull) == 0:
            avg = 0
        else:
            avg = int(np.array(quantity_list_nonull).mean())
        quantity_list = [
            predeict_result.loc[temp_ind, 'before' + str(i)] if
            predeict_result.loc[temp_ind, 'before' + str(i)] != -1 else avg for i in range(1, 7)]

        for i in range(0, 5):
            predeict_result.loc[temp_ind, 'avg_by2_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1]) / 2)
        for i in range(0, 4):
            predeict_result.loc[temp_ind, 'avg_by3_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1] + quantity_list[i + 2]) / 3)
        for i in range(0, 3):
            predeict_result.loc[temp_ind, 'avg_by4_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1] + quantity_list[i + 2] + quantity_list[i + 3]) / 4)
        for i in range(0, 2):
            predeict_result.loc[temp_ind, 'avg_by5_' + str(i + 1)] = int(
                (quantity_list[i] + quantity_list[i + 1] + quantity_list[i + 2] + quantity_list[i + 3] + quantity_list[
                    i + 4]) / 5)

        predeict_result.loc[temp_ind, 'avg_by6_1'] = int(np.array(quantity_list).mean())
    print('-----------')
# predect_x = std.fit_transform(predect_x)

print('success!')
predeict_result.to_csv('/Users/t-mac/desktop/xiecheng/0424/test_final_extratree.csv', index=False)
final_data.to_csv('/Users/t-mac/desktop/xiecheng/0424/extratree.txt', index=False)
