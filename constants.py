from enum import Enum


# константы для кортежа свойств объектов определенного типа
COLOR = 0
FORM = 1
POINT = 2


# перчислимые типы для обозначения типов объектов
# формы объектов
# состояние работы - для объединения объектов
TypeObject = Enum('TypeObject', 'table, chair, bench,'
                                'summerhouse, bathhouse, house,'
                                'tiles, asphalt, grass,'
                                'flower, bush, tree')
Form = Enum('Form', 'polygon, oval')
Select = Enum('Select', 'one, no_one, distance')


# Списки возможных объектов по типу объекта
# Для выбора пользователем
list_furniture = ["стол", "стул", "лавочка"]
list_build = ["беседка", "баня", "дом"]
list_coverage = ["плитка", "асфальт", "трава"]
list_plant = ["цветок", "куст", "дерево"]


# словарь соответсвия выбора объекта и его типа
dict_object = {"стол": TypeObject.table,
               "стул": TypeObject.chair,
               "лавочка": TypeObject.bench,
               "беседка": TypeObject.summerhouse,
               "баня": TypeObject.bathhouse,
               "дом": TypeObject.house,
               "плитка": TypeObject.tiles,
               "асфальт": TypeObject.asphalt,
               "трава": TypeObject.grass,
               "цветок": TypeObject.flower,
               "куст": TypeObject.bush,
               "дерево": TypeObject.tree}


# словарь свойств объектов различного типа
about_object = {TypeObject.table: ("#A0522D", Form.polygon,
                                   [(0, 0), (0, 20), (20, 20), (20, 0)]),
                TypeObject.chair: ("#A0522D", Form.oval,
                                   [(0, 0), (7, 7)]),
                TypeObject.bench: ("#A0522D", Form.polygon,
                                   [(0, 0), (0, 25), (7, 25), (7, 0)]),
                TypeObject.summerhouse: ("#800000", Form.oval,
                                         [(0, 0), (35, 35)]),
                TypeObject.bathhouse: ("#000080", Form.polygon,
                                       [(0, 0), (0, 70), (50, 70), (50, 0)]),
                TypeObject.house: ("#000000", Form.polygon,
                                   [(0, 0), (0, 100), (100, 100), (100, 0)]),
                TypeObject.tiles: ("#C0C0C0", Form.polygon,
                                   [(0, 0), (0, 10), (10, 10), (10, 0)]),
                TypeObject.asphalt: ("#808080", Form.polygon,
                                     [(0, 0), (0, 10), (10, 10), (10, 0)]),
                TypeObject.grass: ("#228B22", Form.polygon,
                                   [(0, 0), (0, 10), (10, 10), (10, 0)]),
                TypeObject.flower: ("#FF1493", Form.oval,
                                    [(0, 0), (5, 5)]),
                TypeObject.bush: ("#3CB371", Form.oval,
                                  [(0, 0), (9, 9)]),
                TypeObject.tree: ("#006400", Form.oval,
                                  [(0, 0), (15, 15)])}
