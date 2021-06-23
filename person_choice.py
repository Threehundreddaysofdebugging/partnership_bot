import json


def selector(price, n):
    k = 1  # цена 1 подписчика
    res = []
    s = []
    with open('db') as f:  # TODO правильное имя файла
        db = json.load(f)
    for key in db.keys():
        s.append((key, db[key]))
    s.sort(key=lambda v: v[1])
    for i in range(len(s)):  # TODO адекватный алгоритм подбора людей
        if s[i][1] * k <= price:
            res = [v[0] for v in s[i:i + 2]]

    return res  # вернет список из 3 людей с ценой меньшей данной


def show_lst(n):
    with open('db') as f:  # TODO правильное имя файла
        db = json.load(f)