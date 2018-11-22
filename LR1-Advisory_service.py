# -*- coding: utf-8 -*-
#@author: Anatoliy
from math import sqrt
import matplotlib.pyplot as plt
import xlrd

#   ./jester-data-1.xls
#   ./test.xlsx

learnData = []
testData = []
numberRatings = []#количество оценок

# Загрузка данных
def load_data(path):
    prefs = []#общий список    
    excelFile = xlrd.open_workbook(path)
    excelList = excelFile.sheet_by_index(0)
    excelRow = excelList.nrows    
    numberObject = len(excelList.row(0))#количество объектов   
    locNumberRatings = 0#количество оценок
    #идем по строчкам
    for rowNumber in range(0, excelRow):  
        arrCell = []           
        #идем по cell
        for cell in range(1, len(excelList.row(rowNumber))):
            #собираем массив cell
            arrCell.append(excelList.row(rowNumber)[cell].value)
            #сумма оценок в строке
            if cell < 99:
                locNumberRatings += 1
        #добавляем массив cell
        prefs.append(arrCell)
        #количество шуток (самая большая строка)
        if len(excelList.row(rowNumber)) > numberObject:
            numberObject = len(excelList.row(rowNumber)) 
        print(excelRow - rowNumber)
    print('\nКоличество пользователей: ', excelRow)
    print('Количество шуток: ', numberObject)
    print('Количество оценок: ', locNumberRatings)
    numberRatings.append(locNumberRatings)
    segmentationData(prefs)
    return prefs

#делим данные
def segmentationData(prefs):
    k = round(len(prefs) * 0.8) 
    for item in range(0, k):
        learnData.append(prefs[item])
    for item in range(k, len(prefs)):
        testData.append(prefs[item])
    pass

# Визуализация матрицы R
def visualize_R(prefs):
    x = []
    y = []
    u = 0
    j = 0
    for user in prefs:      
        for jester in user:       
            x.append(int(u))
            if jester < 99:
                y.append(int(j))  
            else:
                y.append(int(0))
            j += 1 
        u += 1
        j = 0
    plt.plot(x, y, ',')
    plt.show()
    
# реализация функции близости (евклидово расстояние)
def sim_distance_1(prefs, person1, person2):    
    si = {} #получить список предметов, оцененных обоими
    squares = []#квадраты разностей
    i = 0
    while i < len (prefs[person1]):
        if prefs[person1][i] < 99 and prefs[person2][i] < 99:
            #сравниваем если оба оценили
            squares.append(pow(prefs[person1][i] - prefs[person2][i], 2))
            si[i] = 1
        i += 1
    #если нет ни одной общей оценки, вернуть 0    
    if len(si) == 0: return 0
    #сложить квадраты разностей
    return 1/(1+sum(squares))

# реализация функции близости 2 (коэффициент Жаккара)
def sim_distance_2(prefs, person1, person2):
    sM = 0 #получить список предметов, оцененных обоими
    s1 = 0
    s2 = 0
    i = 0
    while i < len (prefs[person1]):
        if prefs[person1][i] < 99 and prefs[person2][i] < 99:
            sM += 1#колличесство общих шуток
        elif prefs[person1][i] != 99:
            s1 += 1
        elif prefs[person2][i] != 99:
            s2 += 1
        i += 1
    return (sM/(s1+s2))

# Возвращает отранжированных k пользователей    
def topMatches(prefs, person, object_id, k=5, similarity=sim_distance_1):
    # собираем список ближайших объектов с оценкой нужного нам object_id (prefs[other][object_id] < 99)
    #цена, оценка, id
    scores = [(similarity(prefs, person, other), prefs[other][object_id], other)    
                        for other in range(0, len(prefs)) if other!=person and prefs[other][object_id] < 99]
    scores.sort()
    scores.reverse()
    return scores[0:k]

# Получить неизвестную оценку объекта для пользователя
def get_rating(prefs, person, object_id, similarity=sim_distance_1):
    # Получаем наиболее похожих пользователей
    scores = topMatches(prefs, person, object_id, similarity=similarity)
    # Если для пользователя не нашлось похожих пользователей (белая ворона), то вернуть 0
    if len(scores) == 0: return 0
    # Вычисляем сумму произведений оценок на меру близости
    sum_sim_score = sum(score[0] * score[1] for score in scores)
    # Вычисляем сумму всех мер близости
    sum_sims = sum(score[0] for score in scores)
    # Вычисляем рейтинг
    rating = sum_sim_score / sum_sims
    return rating

# Расчет среднеквадратической ошибки
def calculate_error(rating_real, rating_predict):
    sum = 0
    for i in range(len(rating_real) - 1):
        sum += pow(rating_real[i] - rating_predict[i], 2)
        sum = sum / numberRatings[0]
    return sqrt(sum)

# Тестирование разработанной системы на тестовой выборке
def test_data():
    #загружаем данные
    pathData = input('Путь к данным: ')
    load_data(pathData)
    #визуализация
    visualize_R(learnData)
    # вычисляем неизвестные оценки
    rating_real = []
    rating_predict1 = []#Пифигор
    rating_predict2 = []#Жаккар
    user = 0
    jester = 0
    while user < len(testData):
        while jester < len(testData[user]):
            rating_real.append(testData[user][jester])
            rating_predict1.append(get_rating(learnData, user, jester, similarity=sim_distance_1))
            rating_predict2.append(get_rating(learnData, user, jester, similarity=sim_distance_2))
            jester += 1
        user += 1
    # вычисляем ошибку RMSE
    print(calculate_error(rating_real, rating_predict1))
    print(calculate_error(rating_real, rating_predict2))
    pass

test_data()
