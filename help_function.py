from math import *


# поворот одного вектора на угол
def vector_rotation(cx, cy, x0, y0, alpha):
    x = cx + (x0 - cx) * cos(alpha) - (y0 - cy) * sin(alpha)
    y = cy + (x0 - cx) * sin(alpha) + (y0 - cy) * cos(alpha)
    return x, y


# расчёт новых координат по списку старых
def new_coordinates(cx, cy, points, alpha):
    new_points = []
    for i in range(0, len(points), 2):
        x0, y0 = vector_rotation(cx, cy, points[i], points[i+1], alpha)
        new_points.extend([x0, y0])
    return new_points


# получение ключа по значению в словаре
def key_by_value(dict, value):
    list_elem = dict.items()
    for i in list_elem:
        if i[1] == value:
            return i[0]


# кортеж точек из списка координат
def tuple_from_list(list_point):
    result = []
    for i in range(0, len(list_point), 2):
        result.append((list_point[i], list_point[i+1]))
    return tuple(result)


# расчет новых координат по старым и сдвигу
def new_point(point, x, y):
    point0 = []
    for i in point:
        point0.append(i[0] + x)
        point0.append(i[1] + y)
    return point0
