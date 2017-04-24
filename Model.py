from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.cross_validation import train_test_split
import numpy as np
from sklearn import linear_model
from sklearn import metrics
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import LinearSVC
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import SGDRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import datetime
from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor, ExtraTreesRegressor
from sklearn.svm import LinearSVR
from xgboost import XGBClassifier
from xgboost import XGBRegressor
from sklearn.feature_extraction import DictVectorizer
from sklearn.grid_search import GridSearchCV

import scipy as sp


def rmse(y_test, y):
    return sp.sqrt(sp.mean((y_test - y) ** 2))


def randomforest(x_train, y_train, x_test, y_test):
    # 随机森林1
    model1 = RandomForestRegressor(n_estimators=1000, max_depth=7, max_features=0.2, max_leaf_nodes=100)
    model1.fit(x_train, y_train)
    model1_y_predict = model1.predict(x_test)

    feat_labels = x_train.columns
    importances = model1.feature_importances_

    indices = np.argsort(importances)[::-1]  # 从大到小排序
    for f in range(0, x_train.shape[1]):
        print(feat_labels[indices[f]], importances[indices[f]])
    sns.set(style="white", context="talk")
    plt.figure()
    plt.title("Feature importances")
    plt.bar(range(x_train.shape[1]), importances[indices],
            color="r", align="center")
    plt.xticks(range(x_train.shape[1]), feat_labels[indices], rotation=90)
    plt.xlim([-1, x_train.shape[1]])
    plt.show()

    print("rfm1 error ", int(mean_absolute_error(y_test, model1_y_predict)))
    print("rfm1 error ", int(mean_squared_error(y_test, model1_y_predict)))
    print('rmse:', rmse(y_test, model1_y_predict))

    return model1


def extratrees(x_train, y_train, x_test, y_test):
    # 极端随机树171
    # model2 = ExtraTreesRegressor(n_estimators=1000, max_depth=12, max_features=0.3, max_leaf_nodes=400)
    model2 = ExtraTreesRegressor(n_estimators=1000, max_depth=20, max_features=0.3, max_leaf_nodes=800)

    model2.fit(x_train, y_train)
    model2_y_predict = model2.predict(x_test)

    print("extraTrees mean_absolute_error:", mean_absolute_error(y_test, model2_y_predict))
    print("extraTrees mean_squared_error:", mean_squared_error(y_test, model2_y_predict))
    print('extraTrees rmse:', rmse(y_test, model2_y_predict))

    return model2


def xgboostmodel1(x_train, y_train, x_test, y_test):
    # XGBoost1
    model4 = XGBRegressor(n_estimators=600, learning_rate=0.01, max_depth=6, colsample_bytree=0.7, subsample=0.7,
                          colsample_bylevel=0.7)
    model4.fit(x_train, y_train)
    model4_y_predict = model4.predict(x_test)

    print("xgboost1 mean_absolute_error:", mean_absolute_error(y_test, model4_y_predict))
    print("xgboost1 mean_squared_error: ", mean_squared_error(y_test, model4_y_predict))
    print('xgboost1 rmse:', rmse(y_test, model4_y_predict))

    return model4


def xgboostmodel2(x_train, y_train, x_test, y_test):
    # XGBoost2
    model5 = XGBRegressor(n_estimators=600, learning_rate=0.01, max_depth=6, colsample_bytree=0.7, subsample=0.7,
                          colsample_bylevel=0.7, seed=10000)
    model5.fit(x_train, y_train)
    model5_y_predict = model5.predict(x_test)

    print("xgboost2 mean_absolute_error:", mean_absolute_error(y_test, model5_y_predict))
    print("xgboost2 mean_squared_error:", mean_squared_error(y_test, model5_y_predict))
    print('xgboost2 rmse:', rmse(y_test, model5_y_predict))

    return model5


def svm_model(x_train, y_train, x_test, y_test):
    # svm
    model7 = LinearSVR(tol=1e-7)
    model7.fit(x_train, y_train)
    model7_y_predict = model7.predict(x_test)

    print("svm mean_absolute_error:", mean_absolute_error(y_test, model7_y_predict))
    print("svm mean_squared_error:", mean_squared_error(y_test, model7_y_predict))
    print('svm rmse:', rmse(y_test, model7_y_predict))

    return model7


def svm_model2(x_train, y_train, x_test, y_test):
    # svm 线性核函数
    model8 = SVR(kernel='linear', tol=1e-7)
    model8.fit(x_train, y_train)
    model8_y_predict = model8.predict(x_test)

    print("svm mean_absolute_error:", mean_absolute_error(y_test, model8_y_predict))
    print("svm mean_squared_error:", mean_squared_error(y_test, model8_y_predict))
    print('svm rmse:', rmse(y_test, model8_y_predict))

    return model8


def svm_model3(x_train, y_train, x_test, y_test):
    # svm径向基核函数
    model9 = SVR(kernel='rbf')
    model9.fit(x_train, y_train)
    model9_y_predict = model9.predict(x_test)

    print("svm mean_absolute_error:", mean_absolute_error(y_test, model9_y_predict))
    print("svm mean_squared_error:", mean_squared_error(y_test, model9_y_predict))
    print('svm rmse:', rmse(y_test, model9_y_predict))

    return model9


def lr_model3(x_train, y_train, x_test, y_test):
    # svm径向基核函数
    model9 = LinearRegression(penalty='l1')
    model9.fit(x_train, y_train)
    model9_y_predict = model9.predict(x_test)

    print("lr_model3 mean_absolute_error:", mean_absolute_error(y_test, model9_y_predict))
    print("lr_model3 mean_squared_error:", mean_squared_error(y_test, model9_y_predict))
    print('lr_model3 rmse:', rmse(y_test, model9_y_predict))
    print('lr_model3 accuracy:', model9.score(x_train, y_train))

    return model9


def xgboostmodel3(x_train, y_train, x_test, y_test):
    # XGBoost3
    # model6 = XGBRegressor(n_estimators=600, learning_rate=0.01, max_depth=6, colsample_bytree=0.7, subsample=0.7,
    #                       colsample_bylevel=0.7)
    model6 = XGBRegressor(n_estimators=600, learning_rate=0.01, max_depth=6, colsample_bytree=0.7, subsample=0.7,
                          colsample_bylevel=0.7, eta=0.05, silent=1)
    model6.fit(x_train, y_train)
    model6_y_predict = model6.predict(x_test)

    print("xgboost3 mean_absolute_error:", mean_absolute_error(y_test, model6_y_predict))
    print("xgboost3 mean_squared_error:", mean_squared_error(y_test, model6_y_predict))
    print('xgboost3 rmse:', rmse(y_test, model6_y_predict))

    return model6


def xgboostmodel4(x_train, y_train, x_test, y_test):
    # XGBoost3
    # model6 = XGBRegressor(n_estimators=600, learning_rate=0.01, max_depth=6, colsample_bytree=0.7, subsample=0.7,
    #                       colsample_bylevel=0.7)
    model6 = XGBRegressor(n_estimators=1600, learning_rate=0.03, max_depth=5, objective='reg:linear',
                          reg_alpha=1, reg_lambda=0)
    model6.fit(x_train, y_train)
    model6_y_predict = model6.predict(x_test)

    print("xgboost3 mean_absolute_error:", mean_absolute_error(y_test, model6_y_predict))
    print("xgboost3 mean_squared_error:", mean_squared_error(y_test, model6_y_predict))
    print('xgboost3 rmse:', rmse(y_test, model6_y_predict))

    return model6


    # std = StandardScaler()
    # X_train = std.fit_transform(X_train)
    # X_test = std.fit_transform(X_test)
    #
    # randomforest(X_train, y_train, X_test, y_test)
    # print('---------------')
    # extraTrees(X_train, y_train, X_test, y_test)
    # print('---------------')
    # xgboostmodel1(X_train, y_train, X_test, y_test)
    # print('---------------')
    # xgboostmodel2(X_train, y_train, X_test, y_test)
    # print('---------------')
    # xgboostmodel3(X_train, y_train, X_test, y_test)
    # print('---------------')
    # svm_model(X_train, y_train, X_test, y_test)
