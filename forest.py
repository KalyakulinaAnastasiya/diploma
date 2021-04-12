import numpy as np
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score

def add(line, line2, x_table):
    if len(line) > len(line2):
        line1 = line
        line = line2
        line2 = line1
    num_row = len(x_table[:, ])
    x = np.zeros((num_row, len(line) + len(line2)), dtype=float)
    y = np.zeros((1, len(line) + len(line2)), dtype=float)
    i = 0
    j = 0
    while i < len(line):
        x[:, j] = x_table[:, line[i]]
        y[0, j] = 1
        j += 1
        x[:, j] = x_table[:, line2[i]]
        y[0, j] = 0
        j += 1
        i += 1
    while i < len(line2):
        x[:, j] = x_table[:, line2[i]]
        y[0, j] = 0
        j += 1
        i += 1

    matrix = np.hsplit(x, [130])
    matrix_y = np.hsplit(y, [130])

    learn = matrix[0]
    test = matrix[1]
    learn_y = matrix_y[0]
    test_y = matrix_y[1]
    learn = learn.transpose()
    learn_y = learn_y.transpose()
    test = test.transpose()
    test_y = test_y.transpose()
    x_learn = np.hsplit(x, [130])

    model = RandomForestClassifier(n_estimators=100,
                                   bootstrap=True,
                                   max_features='sqrt')
    # Обучаем на тренировочных данных
    model.fit(learn, learn_y)
    # Действующая классификация
    rf_predictions = model.predict(test)
    # Вероятности для каждого класса
    rf_probs = model.predict_proba(test)[:, 1]
    roc_value = roc_auc_score(test_y, rf_probs)
    return roc_value

with open('x_table', 'rb') as handle:
    x_table = pickle.load(handle)
with open('dictinary', 'rb') as handle:
    dict = pickle.load(handle)

line = dict['GBR']
line2 = dict['IBS']
line3 = dict['FIN']
line4 = dict['TSI']

var = add(line, line2, x_table)
print("Точность для пары англичане-испанцы:", var)
var = add(line, line3, x_table)
print("Точность для пары англичане-финны:", var)
var = add(line, line4, x_table)
print("Точность для пары англичане-итальянцы:", var)
var = add(line3, line2, x_table)
print("Точность для пары финны-испанцы:", var)
var = add(line4, line2, x_table)
print("Точность для пары итальянцы-испанцы:", var)
var = add(line4, line3, x_table)
print("Точность для пары финны-итальянцы:", var)




