# 携程比赛：出行产品未来14个月销量预测

RMSE：167
比赛链接：https://www.kesci.com/apps/home_log/index.html#!/competition/58bfc27471db03332e1b8a36/content/1

身为菜鸟的我第一次完整的做比赛，断断续续的20多天时间左右，虽然结果并不理想，但是也算是收获颇多。

## 说明：
tools.py：工具类，一些方法
train_processing.py：处理训练集数据特征化
test_processing_new_feature.py：处理预测数据特征化
Model.py：各种单模型，RF，xgboost，ExtraTrees等
model_fit_original：训练，将预测数据写入文件

## 特征工程：

| 特征 | 说明 |
| --- | --- |
| Before1  | 前一个月的销量 |
| Before2 | 前两个月的销量 |
| Before3 | 前三个月的销量 |
| Before4 | 前四个月的销量 |
| Before5 | 前五个月的销量 |
| Before6 | 前六个月的销量 |
| avg_by2 | 每两个月的滑动平均值，5维特征 |
| avg_by3 | 每三个月的滑动平均值，4维特征 |
| avg_by4 | 每四个月的滑动平均值，3维特征 |
| avg_by5 | 每五个月的滑动平均值，2维特征 |
| avg_by6 | 每六个月的滑动平均值，1维特征 |
| count_holiday  | 该月份放假天数：周末加节日 |
| kind_of_holiday0 | 该月份无放假节日 |
| kind_of_holiday1 | 有3天长假 |
| kind_of_holiday2 | 7天长假 |
| eval | 官方评级 |
| eval2 | 携程评级 |
| eval3 | 用户评级 |
| eval4 | 综合评分  |
| voters | 点评人数 |
| location | 地区哑变量 |
| avg_month_quantity | 商品每个月平均销量 |
| avg_month_order | 商品每个月平均预定量 |
| avg_price | 商品平均价格 |
| purchase_rate | 商品购买率：销量／预定量  |

随机森林选择出来的特征权重：
![](http://upload-images.jianshu.io/upload_images/2127249-20f4e7603114d43d.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)



## 尝试过多模型融合 
GBDT+RF+xgboost+Extratrees模型封装
![](http://upload-images.jianshu.io/upload_images/2127249-5f6a9f3f5a122192.jpg?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

没有明显提升

## 结语
时间有限，有很多可以改进的地方，还有很多想法都没付出实现。代码写的也不规范，很多地方写的很蠢，希望看到的童鞋多多交流，多多指导，共同进步。

