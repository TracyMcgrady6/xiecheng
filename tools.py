import datetime
import pandas as pd
import requests
import calendar


def read_file(location):
    return pd.read_csv(location)


def date_range(begin, end, time_regex='%Y-%m'):
    """
        生成begin到end的每一个月的一个list
    :param
        begin: str 开始时间
        end: str 结束时间
        time_regex: str 时间格式的正则表达式
    :argument
        begin需要小于等于end
    :return:
        day_range: list
    --------
        如 date_range('201501', '201502')返回 ['2015-01', '2015-02']
    """
    day_range = []
    day = datetime.datetime.strptime(begin, time_regex).date()
    while True:
        day_str = datetime.datetime.strftime(day, time_regex)
        day_range.append(day_str)
        if day_str == end:
            break
        day = day + datetime.timedelta(days=1)

    return sorted(list(set(day_range)))


def date_range_day(begin, end, time_regex='%Y-%m-%d'):
    """
        生成begin到end的每一天的一个list
    :param
        begin: str 开始时间
        end: str 结束时间
        time_regex: str 时间格式的正则表达式
    :argument
        begin需要小于等于end
    :return:
        day_range: list
    --------
        如 date_range_day('2014-01-01','2014-01-04')返回 ['2014-01-01', '2014-01-02', '2014-01-03', '2014-01-04']
    """
    day_range = []
    day = datetime.datetime.strptime(begin, time_regex).date()
    while True:
        day_str = datetime.datetime.strftime(day, time_regex)
        day_range.append(day_str)
        if day_str == end:
            break
        day = day + datetime.timedelta(days=1)

    return sorted(list(set(day_range)))


# 转化日期格式
def trans_day(day_str, time_regex='%Y/%m/%d'):
    t = datetime.datetime.strptime(day_str, time_regex)
    day_str = datetime.datetime.strftime(t, time_regex)
    return day_str


def trans_day_2(day_str, time_regex='%Y/%m/%d'):
    t = datetime.datetime.strptime(day_str, time_regex)
    day_str = datetime.datetime.strftime(t, '%Y-%m-%d')
    return day_str


def isholiday(date):
    """
    判断是否是节假日
    :param
        date: str 日期
    :returns:
        relust:str 返回值
    --------
        如 isholiday('2017-01-01')返回2
        0:代表工作日
        1：代表周末
        2：代表节日
    """
    relust = requests.get('http://www.easybots.cn/api/holiday.php?d=%s' % date).content.decode(encoding='utf-8')[-3:-2]
    return relust


def count_of_weekendsandholiday(date):
    """
    返回某个月放假天数
    :param
        date: str 日期
    :returns:
        count:int 返回某个月放假天数
    --------

    """
    year = int(date[:4])
    month = int(date[5:7])
    count = 0
    for i in range(calendar.monthrange(year, month)[1] + 1)[1:]:
        day = str(datetime.datetime.strptime(date + '-' + str(i), '%Y-%m-%d'))[:10]
        if int(isholiday(day)) != 0:
            count += 1
    return count


def move_day(day_str, offset, time_regex='%Y/%m/%d'):
    """
        计算day_str偏移offset天后的日期
    :param
        day_str: str 原时间
        offset: str 要偏移的天数
        time_regex: str 时间字符串的正则式
    :return:
        day_str: str 运算之后的结果时间, 同样以time_regex的格式返回
    --------
        如 move_day('20151228', 1)返回 '20151229'
    """
    day = datetime.datetime.strptime(day_str, time_regex).date()
    day = day + datetime.timedelta(days=offset)
    day_str = datetime.datetime.strftime(day, time_regex)
    return day_str


def move_month(day_str, offset):
    """
        计算day_str偏移offset天后的日期
    :param
        day_str: str 原时间
        offset: str 要偏移的天数
        time_regex: str 时间字符串的正则式
    :return:
        day_str: str 运算之后的结果时间, 同样以time_regex的格式返回
    --------
        如 move_day('201512', 1)返回 '201601'
        如 move_day('201512', -1)返回 '201511'
    """
    year = int(day_str[:4])
    month = int(day_str[5:7])
    if month + offset > 12:
        res_month = month + offset - 12
        res_year = year + 1
    elif month + offset < 1:
        res_month = month + offset + 12
        res_year = year - 1
    else:
        res_month = month + offset
        res_year = year
    month_str = str(datetime.datetime.strptime(str(res_year) + '-' + str(res_month), '%Y-%m'))[:7]
    return month_str


weekandholiday = {'2015-01': 10, '2015-02': 11, '2015-03': 9, '2015-04': 9, '2015-05': 11, '2015-06': 9, '2015-07': 8,
                  '2015-08': 10, '2015-09': 8, '2015-10': 13, '2015-11': 9, '2016-01': 11, '2016-07': 10, '2016-06': 9,
                  '2016-12': 9, '2016-03': 8, '2016-08': 8, '2016-02': 11, '2016-09': 9, '2016-11': 8, '2015-12': 8,
                  '2017-01': 12, '2016-10': 13, '2016-05': 10, '2016-04': 10, '2014-09': 8, '2014-12': 8, '2014-08': 10,
                  '2014-10': 12, '2014-11': 10, '2014-07': 8}
# 包含长假期2，短假期1，没有假期0
kindofholiday = {'2015-01': 1, '2015-02': 2, '2015-03': 0, '2015-04': 1, '2015-05': 2, '2015-06': 0, '2015-07': 0,
                 '2015-08': 0, '2015-09': 1, '2015-10': 2, '2015-11': 0, '2016-01': 1, '2016-07': 0, '2016-06': 1,
                 '2016-12': 0, '2016-03': 0, '2016-08': 0, '2016-02': 2, '2016-09': 1, '2016-11': 0, '2015-12': 0,
                 '2017-01': 2, '2016-10': 2, '2016-05': 1, '2016-04': 1, '2014-07': 0, '2014-08': 0, '2014-09': 2,
                 '2014-10': 2, '2014-11': 1, '2014-12': 0}
