from sklearn.linear_model import LogisticRegressionCV
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
from sklearn.svm import SVC
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import numpy as np

from langdetect import DetectorFactory
from langdetect import detect

import os

filter=[".json"] #设置过滤后的文件类型 当然可以设置多个类型

def all_path(dirname):

    result = []#所有的文件

    for maindir, subdir, file_name_list in os.walk(dirname):

        # print("1:",maindir) #当前主目录
        # print("2:",subdir) #当前主目录下的所有目录
        # print("3:",file_name_list)  #当前主目录下的所有文件

        for filename in file_name_list:
            apath = os.path.join(maindir, filename)#合并成一个完整路径
            ext = os.path.splitext(apath)[1]  # 获取文件后缀 [0]获取的是除了文件名以外的内容

            if ext in filter:
                result.append(apath)

    return result




def is_leap_year(year):
    """
      判断当前年份是不是闰年，年份公元后，且不是过大年份
      :param year: 年份
      :return: True 闰年， False 平年
      """
    if year % 4 == 0 and year % 100 != 0 or year % 400 == 0:
        return True
    return False


def get_month(month_str):
    """
    把输入 月份字符串缩写转化成整数
    :param month_str:  月份:JAN,FEB，MAR,APR...
    :return: 对应月份整数：1,2,3,4...
    """
    if month_str == "Jan": return 1
    if month_str == "Feb": return 2
    if month_str == "Mar": return 3
    if month_str == "Apr": return 4
    if month_str == "May": return 5
    if month_str == "Jun": return 6
    if month_str == "Jul": return 7
    if month_str == "Aug": return 8
    if month_str == "Sep": return 9
    if month_str == "Sept": return 9
    if month_str == "Oct": return 10
    if month_str == "Nov": return 11
    if month_str == "Dec": return 12


def get_day_of_year(year, month, day):
    """
    获取一个日期在这一年中的第几天
    :param year: 年份
    :param month: 月份
    :param day: 日期
    :return: 在这一年中的第几天
    """
    month_of_days31 = [1, 3, 5, 7, 8, 10, 12]
    month_of_days30 = [4, 6, 9, 11]

    if month == 1:
        return day

    if month == 2:
        return day + 31

    days_of_31_num = 0
    days_of_30_num = 0
    # 31天月份数
    for days_of_31 in month_of_days31:
        if days_of_31 < month:
            days_of_31_num += 1
        else:
            break

    # 30天月份数
    for days_of_30 in month_of_days30:
        if days_of_30 < month:
            days_of_30_num += 1
        else:
            break

    return days_of_31_num * 31 + days_of_30_num * 30 + (29 if is_leap_year(year) else 28) + day

def LogisticRegression(data, cv_fold=2):
    # print(data.X.__sizeof__(),data.Y.__sizeof__())
    X_train, X_test, Y_train, Y_test = train_test_split(data.X, data.Y, test_size=0.05)
    lr = LogisticRegressionCV(Cs=np.logspace(-4, 1, 50), cv=cv_fold, fit_intercept=True, penalty="l2",
                              solver="lbfgs", tol=0.01, multi_class="multinomial")
    lr.fit(X_train, Y_train)
    prediction = lr.predict(X_test)
    print("prediction=", prediction)
    print("results=", Y_test)
    print(classification_report(Y_test, prediction))

def svm_basic(data):
    clf = SVC(gamma='auto')
    X_train, X_test, Y_train, Y_test = train_test_split(data.X, data.Y, test_size=0.05)
    clf.fit(X_train, Y_train)
    prediction = clf.predict(X_test)
    print(classification_report(Y_test, prediction))


def lang_detect(text):
    DetectorFactory.seed = 0
    try:
        return detect(text)
    except:
        return "null"
