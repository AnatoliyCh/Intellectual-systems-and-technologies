# -*- coding: utf-8 -*-
import os
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cross_validation import train_test_split
from sklearn.naive_bayes import BernoulliNB, MultinomialNB, GaussianNB
from sklearn import metrics

all_data = [] #массив всех данных

def loadData(): #загрузка данных из файлов
    global all_data
    dir_paths = ['./LR2-Data/neg/', './LR2-Data/pos/']    
    for dir_path in dir_paths:
        for filename in os.listdir(dir_path):
            with open(dir_path + "/" + filename, 'r') as content_file:
                all_data.append([content_file.read(), dir_paths.index(dir_path)])
        print ("READ", len(os.listdir(dir_path)), "FILES from", dir_path)

def arrayMerge(oldArr): #слияние массива
    newArr = []
    sz = len(oldArr)
    print(sz)
    k = 0
    for tmp in oldArr:
        k = k + 1        
        tmp = np.delete(tmp, 1, 0)
        newArr = np.concatenate((newArr, tmp), axis=0)
        if (k % 100) == 0:
            print(sz - k)
    return newArr
    
def test(typeBK, maxFeatures):
    global all_arr_merge_data
    global pos_neg_col
    # 4 - преобразование в features vector
    vectorizer = CountVectorizer(analyzer = "word",   \
                                 tokenizer = None,    \
                                 preprocessor = None, \
                                 stop_words = None,   \
                                 max_features = maxFeatures)
    train_data_features = vectorizer.fit_transform(all_arr_merge_data)
    train_data_features = train_data_features.toarray() 
    # 5 - разделение массива на обучающую и тестовую выборки
    X_train, X_test, Y_train, Y_test = train_test_split(train_data_features, pos_neg_col, test_size=0.1, random_state=0)
    if typeBK == "BernoulliNB":
        clf = BernoulliNB()
        clf.fit(X_train, Y_train)
        res = clf.predict(X_test)
        print("max_features:" , maxFeatures, "accuracy_score:", metrics.accuracy_score(Y_test, res))   
    if typeBK == "GaussianNB":
        clf = GaussianNB()
        clf.fit(X_train, Y_train)
        res = clf.predict(X_test)
        print("max_features:" , maxFeatures, "accuracy_score:", metrics.accuracy_score(Y_test, res))   

# 3 - загрузка, объединение, преобразование в массив данных, отделение значений показателей, создание одного масива данных
loadData()
all_arr_data = np.array(all_data)
pos_neg_col = all_arr_data[:,1]
pos_neg_col = pos_neg_col.astype(int)
all_arr_merge_data = arrayMerge(all_arr_data)

# 4 5 6 шаги
#6 - эксперименты и точность
print("BernoulliNB")
test("BernoulliNB", 4000)
test("BernoulliNB", 6000)
test("BernoulliNB", 8000)
print("GaussianNB")
test("GaussianNB", 4000)
test("GaussianNB", 6000)
test("GaussianNB", 8000)



