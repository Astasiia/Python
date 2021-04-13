from tkinter.messagebox import *
from tkinter import filedialog
from interface import *
from help_function import *
from PIL import ImageDraw
from shapely.geometry import Polygon


# класс основного окна приложения
class UserWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Создай свой участок")
        self.geometry('1000x760')
        self["bg"] = "gray90"
        # основное поле для работы (на котором все рисуется)
        self.canvas = WorkingField(self)

    # функция создания кнопок интерфейса
    def create_button(self):
        create_btn_obj(self)
        create_btn_prj(self)
        create_btn_add(self)
        create_btn_garden(self)
        create_btn_function(self)
        # create_btn_move(self)

    ##########
    # функции для работы с проектом

    # создание кнопок с картинками
    # запуск основного цикла работы окна
    def start(self):
        self.create_button()
        work_move_obj = Frame(self, width=250, height=200, bg="lightyellow",
                              bd=5, relief=RIDGE)
        work_move_obj.place(x=290, y=550)
        lbl = Label(work_move_obj,
                    text="Движение объектов холста",
                    font=("Times New Roman", 18),
                    bg="lightyellow")
        image_r = load_image("right.png", 35)
        image_r = ImageTk.PhotoImage(image_r)
        image_l = load_image("left.png", 35)
        image_l = ImageTk.PhotoImage(image_l)
        image_u = load_image("up.png", 35)
        image_u = ImageTk.PhotoImage(image_u)
        image_d = load_image("down.png", 35)
        image_d = ImageTk.PhotoImage(image_d)
        image_r_t = load_image("right_turn.png", 50)
        image_r_t = ImageTk.PhotoImage(image_r_t)
        image_l_t = load_image("left_turn.png", 50)
        image_l_t = ImageTk.PhotoImage(image_l_t)
        btn_left = Button(work_move_obj, width=35, height=35, image=image_l,
                          command=lambda: self.canvas.move_obj("l"))
        btn_right = Button(work_move_obj, width=35, height=35, image=image_r,
                           command=lambda: self.canvas.move_obj("r"))
        btn_up = Button(work_move_obj, width=35, height=35, image=image_u,
                        command=lambda: self.canvas.move_obj("u"))
        btn_down = Button(work_move_obj, width=35, height=35, image=image_d,
                          command=lambda: self.canvas.move_obj("d"))
        btn_left_turn = Button(work_move_obj, width=50, height=50, image=image_l_t,
                               command=lambda: self.canvas.rotation_obj("l"))
        btn_right_turn = Button(work_move_obj, width=50, height=50, image=image_r_t,
                                command=lambda: self.canvas.rotation_obj("r"))
        lbl.place(x=20, y=20)
        btn_left.place(x=20, y=100)
        btn_right.place(x=100, y=100)
        btn_up.place(x=60, y=60)
        btn_down.place(x=60, y=140)
        btn_left_turn.place(x=170, y=60)
        btn_right_turn.place(x=170, y=130)
        self.mainloop()

    # события при нажатии Выход
    def close(self):
        ans = askyesno("Выход", "Перед выходом сохраните файл!\n Вы действительноо хотите выйти?")
        if ans:
            self.destroy()

    # события при нажатии Сохранить
    def save_config(self):
        filetypes = [("TXT", "*.txt")]
        new_file = filedialog.asksaveasfilename(filetypes=filetypes)
        if new_file:
            f = open(new_file, 'w')
            # запись конфигурации в файл с холста
            self.canvas.save_config(f)
            f.close()

    # события при нажатии Рисунок
    def save_picture(self):
        filetypes = [("JPG", "*.jpg")]
        new_file = filedialog.asksaveasfilename(filetypes=filetypes)
        if new_file:
            # сохранение объектов с холста картинкой
            self.canvas.save_image(new_file)

    # события при нажатии Загрузить
    def download(self):
        filetypes = [("TXT", "*.txt")]
        file = filedialog.askopenfilename(filetypes=filetypes)
        if file:
            f = open(file, 'r')
            self.canvas.download(f)
            f.close()

    # события при нажатии Информация
    def instruction(self):
        f = open("information.txt")
        text = ""
        x = f.readline()
        while x != "\n":
            text = text + x
            x = f.readline()
        showinfo("Инструкция", text)


# класс поля для работы
class WorkingField(Canvas):
    def __init__(self, window):
        super().__init__(window, width=650, height=500, bg="white")
        self.place(x=20, y=20)
        # объект участка на холсте
        self.garden = None
        # списки элемнтарных и составных объектов на холсте
        self.list_elementary = []
        self.list_combining = []
        # словарь тегов всех объектов на холсте (кроме участка)
        # значения либо None, либо составной объект,
        # содержащий элементарный с данным тегом
        self.all_obj = {}
        # характеристики участка
        # размер и покрытие
        self.vertical_len = 0
        self.horizontal_len = 0
        self.coverage = None
        # координаты левого верхнего угла участка
        self.x = 0
        self.y = 0
        # тег выбранного объекта
        self.select_object = None
        # список тегов выбранных объектов (для объединения)
        self.select_comb = []
        # флаг состояния выбора объекта
        # просто объект или объекты для объединения
        self.select_flag = Select.one
        # основное окно приложения
        self.window = window
        # множества объектов, нарушающих правила
        # пересекающиеся объекты и выходящие за участок
        self.intersection = set()
        self.outside_garden = set()
        # информационный текст для объединения и расчета расстояния
        self.text_merge = None
        self.text_distance = None
        # хранение координат для расчета расстояния между ними
        self.distance_obj = [None, None]
        # объект линия - какое расстояне измеряется
        self.line = None

    ##########
    # функции для создания объектов класса

    # создание элементарного объекта
    def add_elementary(self, type_obj, tag):
        x = ElementaryObject(type_obj, tag, self)
        # оьновление списка и словаря
        self.list_elementary.append(x)
        self.all_obj.update({tag: None})

    # создание составного объекта
    # из списка элементарных
    def add_compound(self, list_item):
        x = CompoundObject(list_item, self)
        # обновление списка и словаря
        self.list_combining.append(x)
        for i in list_item:
            self.all_obj.update({i.tag: x})

    ##########
    # функции для работы с холстом

    # удаление объекта с поля
    def delete_obj(self):
        if self.garden is None:
            return
        if self.check_flag_merge():
            return
        if self.check_flag_distance():
            return
        obj = self.select_object
        self.select_object = None
        if obj is None:
            return
        x = self.all_obj.get(obj)
        if x is None:
            # элементарный объект просто удаляем
            self.delete(obj)
            # обновление списка и словаря
            for i in self.list_elementary:
                if obj == i.tag:
                    self.list_elementary.remove(i)
                    break
            self.all_obj.pop(obj)
        else:
            # для составного удаляем все элементарные
            for j in x.list_tag:
                self.delete(j)
            # обновление списка и словаря
            self.list_combining.remove(x)
            for j in x.items:
                self.all_obj.pop(j, 0)
        # проверка пересечений после удаления
        self.check_intersection_obj()
        # выделение объектов с пересечениями
        self.error_position()

    # очистка всего поля
    def clear(self):
        # удаление всего с холста
        self.delete(ALL)
        # обновление всех структур и атрибутов
        self.select_object = None
        self.select_comb.clear()
        self.select_flag = Select.one
        self.list_elementary.clear()
        self.list_combining.clear()
        self.vertical_len = 0
        self.horizontal_len = 0
        self.coverage = None
        self.x = 0
        self.y = 0
        self.all_obj.clear()
        self.intersection.clear()
        self.outside_garden.clear()
        self.garden = None
        self.distance_obj = [None, None]
        self.text_merge = None
        self.text_distance = None
        self.line = None

    # объединение объектов в два этапа
    # выделение нужных (после первого нажатия)
    # объединение элементарных в составной (после второго)
    # определение нажатия по флагу объединения
    def merge(self):
        if self.garden is None:
            return
        # проверка на процесс расчета расстояния
        if self.check_flag_distance():
            return
        if self.select_flag == Select.one:
            # первое нажатие
            self.select_flag = Select.no_one
            if self.select_object is not None:
                x = self.all_obj.get(self.select_object)
                # добавляем уже выделенные объекты в список выделенных для объединения
                if x is None:
                    self.select_comb.append(self.select_object)
                else:
                    self.select_comb.extend(x.list_tag)
            # информационное сообщение о процессе объединения
            self.text_merge = self.create_text(300, 10,
                                               text="Выберите объекты для объединения в один",
                                               font="TimesNewRoman")
        else:
            # удаляем сообщение
            self.delete(self.text_merge)
            # второе нажатие
            list_comb = self.select_comb.copy()
            # объединяем все объекты
            self.combining_obj(list_comb)
            # снимаем все выделения на холсте
            self.delete_select()

    # разъединение составного объекта на элементарные
    def separation(self):
        if self.garden is None:
            return
        # проверка на процесс расчета расстояния и объединения
        if self.check_flag_distance():
            return
        if self.check_flag_merge():
            return
        if self.select_object is None:
            # если ничего не выделенно, ничего не делаем
            return
        x = self.all_obj.get(self.select_object)
        if x is None:
            # для элементарного просто убираем выделения
            color = self.itemcget(self.select_object, "fill")
            self.itemconfig(self.select_object, outline=color)
        else:
            # для составного убираем все выделения
            self.item_config_all(self.select_object, None)
            # разбиваем составной на элементарные (обновление структур)
            self.separation_obj(self.select_object)
        self.select_object = None
        # проверка пересечений и выхождения за пределы участка
        self.check_object_on_garden()
        self.check_intersection_obj()
        self.error_position()

    # создание по введенной информации самого участка
    def create_garden(self, in_x, in_y, in_coverage):
        if self.garden is not None:
            # если уже есть, поменять нельзя
            # только после очищения
            return
        # рассчет координат (для расположения в центре)
        x = 10 * int(in_x.get())
        y = 10 * int(in_y.get())
        x0 = 325 - int(x / 2)
        y0 = 250 - int(y / 2)
        # расположение
        self.x = x0
        self.y = y0
        # определение покрытия
        coverage = dict_object.get(in_coverage.get())
        color = about_object.get(coverage)[COLOR]
        self.delete(self.garden)
        # расположение участка (с учетом рамки)
        self.garden = self.create_polygon((x0 - 5, y0 - 5), (x0 + x + 5, y0 - 5), (x0 + x + 5, y0 + y + 5),
                                          (x0 - 5, y0 + y + 5),
                                          outline="black", fill=color, width=5)
        # на задний план
        self.tag_lower(self.garden)
        # характеристика участка
        self.vertical_len = y
        self.horizontal_len = x
        self.coverage = coverage

    def select_new_obj(self, list_obj):
        # выбор нового добавляемого объекта
        if self.garden is None:
            # если нет участка, нельзя выбрать
            return
        # проверка процесса объединения и рассчета
        if self.check_flag_distance():
            return
        if self.check_flag_merge():
            return
        # создание нового дополнительного окна для выбора нового объекта
        create_window_select(self.window, list_obj)

    # движение объекта
    def move_obj(self, direction):
        if self.garden is None:
            return
        # проверка процесса объединения и рассчета
        if self.check_flag_distance():
            return
        if self.check_flag_merge():
            return
        if self.select_object is None:
            # нет выделенного объекта
            return
        x = self.all_obj.get(self.select_object)
        # по типу выделенного объекта просим его двигаться в определенном направлении
        if x is None:
            for i in self.list_elementary:
                if self.select_object == i.tag:
                    i.move(direction)
                    break
        else:
            x.move(direction)

    # поворот объекта
    def rotation_obj(self, direction):
        if self.garden is None:
            return
        # проверка процесса объединения и рассчета
        if self.check_flag_distance():
            return
        if self.check_flag_merge():
            return
        if self.select_object is None:
            # нет выделенного объекта
            return
        x = self.all_obj.get(self.select_object)
        # по типу выделенного объекта просим его поворачиваться в определенном направлении
        if x is None:
            for i in self.list_elementary:
                if self.select_object == i.tag:
                    i.rotation(direction)
                    break
        else:
            x.rotation(direction)

    ##########
    # функции для работы с дополнительными функциями (расстояния, информация)

    # вывод информации по объектам
    def information(self):
        # расчет и вывод
        count_object = self.count_all_object()
        create_info(count_object)

    # запуск процесса расчета расстояния
    # выбор объектов для рассчета
    def distance(self):
        # проверка процесса объеинения
        if self.garden is None:
            return
        if self.check_flag_merge():
            return
        self.delete_select()
        self.select_flag = Select.distance
        self.text_distance = self.create_text(300, 10,
                                              text="Выберите точку на первом объекте для расчета расстояния",
                                              font="TimesNewRoman")

    # сбррос всех выделений и дополнительных обозначений
    # и информационных сообщений
    def drop(self):
        if self.garden is None:
            return
        self.delete(self.line)
        self.delete_select()
        self.delete(self.text_distance)
        self.delete(self.text_merge)

    # проверка пересечений между объектами на участке
    def check_intersection_obj(self):
        # предыдущие пересечения обнуляем
        for i in self.intersection:
            color0 = self.itemcget(i, "fill")
            self.itemconfig(i, outline=color0)
        intersection = set()
        all_elem = list(self.all_obj.keys())
        # по всем объектам на холсте (кроме участка)
        for i in all_elem.copy():
            border = self.coords(i)
            list_intersection = []
            # для круглых
            if len(border) == 4:
                # определяем по центру и радиусу
                # только круглые с круглыми
                c = (0.5 * (border[0] + border[2]), 0.5 * (border[1] + border[3]))
                r = c[0] - border[0]
                for j in all_elem.copy():
                    p = self.coords(j)
                    if len(p) == 4:
                        c1 = (0.5 * (p[0] + p[2]), 0.5 * (p[1] + p[3]))
                        r1 = c1[0] - p[0]
                        if (c1[0] - c[0]) ** 2 + (c1[1] - c[1]) ** 2 < (r + r1) ** 2:
                            list_intersection.append(j)
            # для прямоугольных
            elif len(border) == 8:
                for j in all_elem.copy():
                    p = self.coords(j)
                    if len(p) == 8:
                        point = p
                    elif len(p) == 4:
                        point = polygon_for_circle(p)
                    p1 = Polygon(tuple_from_list(border))
                    p2 = Polygon(tuple_from_list(point))
                    if p1.intersects(p2):
                        list_intersection.append(j)
            # удаляем из списка пересечений участок и линию расстояния
            if list_intersection.count(self.garden) != 0:
                list_intersection.remove(self.garden)
            if (self.line is not None) & (self.line in list_intersection):
                list_intersection.remove(self.line)
            # в пересечнии остался только сам объект, пропускаем
            if len(list_intersection) == 1:
                list_intersection.clear()
                continue
            # обновляем список новых пересечений
            intersection.update(list_intersection)
            list_intersection.clear()
        # обновляем хранимых список пересечний
        self.intersection.clear()
        self.intersection.update(intersection)

    # проверка выхода за границу участка
    def check_object_on_garden(self):
        all_elem = self.all_obj.keys()
        border = self.coords(self.garden)
        list_on_garden = self.find_enclosed(border[0], border[1],
                                            border[4], border[5])
        self.outside_garden.clear()
        # по всем элементам
        for i in all_elem:
            # возвращаем к объекту без выделения
            color = self.itemcget(i, "fill")
            self.itemconfig(i, outline=color)
            # объекты не на участке добавляем в множество вне участка
            if i not in list_on_garden:
                self.outside_garden.add(i)

    # функция отображения на холсте ошибочных расположений объектов
    def error_position(self):
        error = set()
        error.update(self.intersection)
        error.update(self.outside_garden)
        # по всем нарушенным делаем красную рамку
        for i in error:
            self.itemconfig(i, outline="red")
        # возвращаем выделенный объект(ы)
        # если не нарушают ничего
        if self.select_comb:
            for i in self.select_comb:
                self.return_selection(i, error)
        else:
            self.return_selection(self.select_object, error)

    ##########
    # функции для работы с проектом

    # сохранение конфигурации в файл
    def save_config(self, file):
        file.write("GARDEN\n")
        file.write(self.load_garden())
        file.write("ELEMENTARY\n")
        for i in self.list_elementary:
            file.write(i.load_option())
        file.write("COMPOUND\n")
        for i in self.list_combining:
            file.write(i.load_option())
        file.write("\n")

    # загрузка конфигурации из файла
    def download(self, file):
        flag = None
        self.clear()
        while 1:
            i = file.readline()
            if i == "GARDEN\n":
                flag = "g"
                continue
            elif i == "ELEMENTARY\n":
                flag = "e"
                continue
            elif i == "COMPOUND\n":
                flag = "c"
                list_items = []
                continue
            elif i == "\n":
                if list_items:
                    self.combining_obj(list_items)
                return
            if flag == "g":
                coverage = dict_object.get(file.readline().rstrip('\n'))
                point = eval(file.readline())
                self.create_load_garden(coverage, point)
            elif flag == "e":
                type_obj = dict_object.get(file.readline().rstrip('\n'))
                point = eval(file.readline())
                self.create_load_elementary(type_obj, point)
            elif flag == "c":
                if i == "C\n":
                    file.readline()
                    if list_items:
                        self.combining_obj(list_items)
                        list_items.clear()
                type_obj = dict_object.get(file.readline().rstrip('\n'))
                point = eval(file.readline())
                obj = self.create_load_elementary(type_obj, point)
                list_items.append(obj)
            elif flag is None:
                return
        # отображение всех нарушений
        self.check_intersection_obj()
        self.check_object_on_garden()
        self.error_position()

    # сохранение изображения с холста
    def save_image(self, file):
        if self.garden is None:
            return
        image = Image.new("RGB", (600, 400), "white")
        draw = ImageDraw.Draw(image)
        point = tuple_from_list(self.coords(self.garden))
        color0 = self.itemcget(self.garden, "fill")
        color1 = self.itemcget(self.garden, "outline")
        draw.polygon(point, color0, color1)
        elem = self.all_obj.keys()
        for i in elem:
            point = tuple_from_list(self.coords(i))
            color0 = self.itemcget(i, "fill")
            if len(point) == 4:
                draw.polygon(point, color0)
            else:
                draw.ellipse(point, color0)
        image.save(file)

    ##########
    # вспомогательные функции, функции для работы с объектами
    # функции для работы с холстом

    # при отсутсвии ошибок, возврат выделения
    def return_selection(self, obj, error):
        x = self.all_obj.get(obj)
        if x is None:
            if obj not in error:
                self.itemconfig(obj, outline="green2")
        else:
            for i in x.list_tag:
                if i not in error:
                    self.itemconfig(i, outline="green2")

    # объединение объектов в составной
    def combining_obj(self, list_comb):
        list_item = []
        # обработка частей, являющихся элементарными
        for i in self.list_elementary:
            if i.tag in list_comb:
                list_item.append(i)
                list_comb.remove(i.tag)
        for i in list_item:
            self.list_elementary.remove(i)
        # обработка частей, являющихся составными
        compound = []
        list_elem = list_item.copy()
        if list_comb:
            compound = self.separation_for_merge(list_item, list_comb)
        if len(list_item) < 2:
            self.list_elementary.extend(list_elem)
            self.list_combining.extend(compound)
            return
        # добавляем составной объект
        self.add_compound(list_item)

    # разъединение составного на элементраные для нового объединения
    def separation_for_merge(self, item, comb):
        list_comb = []
        while comb:
            x = comb.pop()
            elem = self.all_obj.get(x)
            self.list_combining.remove(elem)
            list_comb.append(elem)
            for j in elem.list_tag:
                if j != x:
                    comb.remove(j)
            for j in elem.items:
                item.append(j)
        return list_comb

    # разъединение объектов
    def separation_obj(self, obj):
        x = self.all_obj.get(obj)
        # обновление списков объектов и словаря
        self.list_combining.remove(x)
        self.list_elementary.extend(x.items)
        for j in x.items:
            self.all_obj.update({j.tag: None})

    # расчет количества объектов различного типа
    def count_all_object(self):
        count_object = {}
        for i in about_object.keys():
            count_object.update({i: 0})
        for i in self.list_elementary:
            count = count_object.get(i.type)
            count_object.update({i.type: count + 1})
        for i in self.list_combining:
            for j in i.items:
                count = count_object.get(j.type)
                count_object.update({j.type: count + 1})
        return count_object

    # расчет расстояния и вывод сообщения на холст
    def show_distance(self):
        self.delete(self.text_distance)
        distance = sqrt((self.distance_obj[0][0] - self.distance_obj[1][0]) ** 2 +
                        (self.distance_obj[0][1] - self.distance_obj[1][1]) ** 2)
        self.text_distance = self.create_text(300, 10,
                                              text="Расстояние: " + str(distance / 10) + " м",
                                              font="TimesNewRoman")
        self.delete(self.line)
        self.line = self.create_line(*self.distance_obj)
        self.distance_obj = [None, None]

    # создание участка по информации из файла
    def create_load_garden(self, coverage, point):
        self.x = point[0] + 5
        self.y = point[1] + 5
        color = about_object.get(coverage)[COLOR]
        self.garden = self.create_polygon(point, outline="black", fill=color, width=5)
        self.tag_lower(self.garden)
        self.vertical_len = point[6] - point[0] - 10
        self.horizontal_len = point[7] - point[1] - 10
        self.coverage = coverage

    # создание элементов по информации из файла
    def create_load_elementary(self, type_obj, point):
        lst = about_object.get(type_obj)
        if lst[FORM] is Form.oval:
            # круглый
            a = self.create_oval(point, fill=lst[COLOR], outline=lst[COLOR],
                                 activeoutline="cyan", width=2)
        else:
            # прямоугольный
            a = self.create_polygon(point, fill=lst[COLOR], outline=lst[COLOR],
                                    activeoutline="cyan", width=2)
        # связь с функцией при нажатии
        self.tag_bind(a, '<Button-1>', lambda event: self.new_select(a, event))
        # добавление элементарного объекта
        self.add_elementary(type_obj, a)
        return a

    # изменение конфигурации составного объекта (цвета)
    def item_config_all(self, obj, color):
        x = self.all_obj.get(obj)
        # по всем объектам, входящим в тот же составной объект
        if color is None:
            # цвет не задан, возвращаем к невыделенному
            for j in x.list_tag:
                color0 = self.itemcget(j, "fill")
                self.itemconfig(j, outline=color0)
        else:
            # при заданном цвете
            for j in x.list_tag:
                self.itemconfig(j, outline=color)

    # удаление всех выделений на холсте
    def delete_select(self):
        # по списку выделенных объектов
        for i in range(0, len(self.select_comb)):
            color = self.itemcget(self.select_comb[i], "fill")
            self.itemconfig(self.select_comb[i], outline=color)
        self.select_comb.clear()
        self.select_object = None
        self.select_flag = Select.one
        # возвращаем все нарушения
        self.check_object_on_garden()
        self.check_intersection_obj()
        self.error_position()

    # рисуем новый объект по характеристикам на холсте
    def draw_object(self, select, window):
        type_obj = dict_object.get(select.get())
        lst = about_object.get(type_obj)
        point = self.point_for_add(lst[POINT])
        if lst[FORM] is Form.oval:
            # круглый
            a = self.create_oval(point, fill=lst[COLOR], outline=lst[COLOR],
                                 activeoutline="cyan", width=2)
        else:
            # прямоугольный
            a = self.create_polygon(point, fill=lst[COLOR], outline=lst[COLOR],
                                    activeoutline="cyan", width=2)
        # связь с функцией при нажатии
        self.tag_bind(a, '<Button-1>', lambda event: self.new_select(a, event))
        # добавление элементарного объекта
        self.add_elementary(type_obj, a)
        window.destroy()
        # выделение добавленного объекта
        self.new_select(a, None)

    # расчёт точек для добавления объекта в левый угол участка
    def point_for_add(self, points):
        result = []
        dx = self.x
        dy = self.y
        for i in points:
            result.append((i[0] + dx, i[1] + dy))
        return result

    # новое выделение на холсте
    def new_select(self, obj, event):
        # процесс расчета расстояния
        if self.select_flag is Select.distance:
            if self.line is not None:
                self.check_flag_distance()
                self.new_select(obj, event)
                return
            # добавление первых и вторых координат для расчета
            if self.distance_obj[0] is None:
                self.distance_obj[0] = (event.x, event.y)
                self.delete(self.text_distance)
                self.text_distance = self.create_text(300, 10,
                                                      text="Выберите точку на втором объекте для расчета расстояния",
                                                      font="TimesNewRoman")
            else:
                self.distance_obj[1] = (event.x, event.y)
                self.select_flag == Select.one
                # запуск расчета после второй точки
                self.show_distance()
            return
        # не объединение
        if self.select_flag is Select.one:
            if self.select_object is not None:
                # возвращаем к невыделению предыдущий выделенный
                x = self.all_obj.get(self.select_object)
                if x is None:
                    color = self.itemcget(self.select_object, "fill")
                    self.itemconfig(self.select_object, outline=color)
                else:
                    self.item_config_all(self.select_object, None)
            if obj is self.select_object:
                # если нажали на выделенный, то ничего не выделено больше
                self.select_object = None
            else:
                # иначе нажатый выделен
                self.select_object = obj
        else:
            # процесс выбора для объединения
            x = self.all_obj.get(obj)
            # выделение одного или всех составляющих (для составного)
            if x is None:
                self.select_elem(obj)
            else:
                for j in x.list_tag:
                    self.select_elem(j)
        # меняем рамку для выделенных
        if self.select_object is not None:
            x = self.all_obj.get(self.select_object)
            if x is None:
                self.itemconfig(self.select_object, outline="green2")
            else:
                self.item_config_all(self.select_object, "green2")
        # проверяем все нарушения
        # нарушения не убираются при выделении данного объекта
        self.check_object_on_garden()
        self.check_intersection_obj()
        self.error_position()

    # функция обновления структур при выделении нового
    # удаление или добавление в список выделенных для объединения
    def select_elem(self, obj):
        x = self.select_comb.count(obj)
        if x:
            self.select_comb.remove(obj)
            color = self.itemcget(obj, "fill")
            self.itemconfig(obj, outline=color)
            self.select_object = None
        else:
            self.select_comb.append(obj)
            self.select_object = obj

    # сброс процесса расчета расстояния
    def check_flag_distance(self):
        if self.select_flag is Select.distance:
            # если процесс расчета расстояния
            # удаляем всю информацию по нему
            self.delete(self.text_distance)
            self.delete(self.line)
            self.text_distance = None
            self.line = None
            self.distance_obj = [None, None]
            self.select_flag == Select.one
            self.delete_select()
            return True
        return False

    # сброс процесса объединени
    def check_flag_merge(self):
        if self.select_flag is Select.no_one:
            # если процесс объединения
            # убираем все выделения, ничего не делаем
            self.delete_select()
            self.delete(self.text_merge)
            return True
        return False

    # загрузка информации об участке в файл
    def load_garden(self):
        if self.garden is None:
            return "\n"
        coverage = key_by_value(dict_object, self.coverage)
        point = str(self.coords(self.garden))
        result = "G\n" + coverage + "\n" + point + "\n"
        return result


# класс составной объект
class CompoundObject:
    def __init__(self, list_item, canvas):
        # холст
        self.canvas = canvas
        # составляющие его элементарные объекты
        self.items = list_item.copy()
        # список тегов составляющих его элементарных объектов
        self.list_tag = []
        for i in list_item:
            self.list_tag.append(i.tag)

    # функция движения составного объекта
    def move(self, direction):
        for i in self.items:
            # перемещение всех составляющих элементарных
            i.move(direction)

    # функция поворота составного объекта
    def rotation(self, direction):
        # повороты на 5 градусов
        if direction == "l":
            alpha = -pi / 36
        elif direction == "r":
            alpha = pi / 36
        # опредеение прямоугольника объединяющего объекты
        xc1, yc1, xc2, yc2 = self.canvas.bbox(*self.list_tag)
        center = (0.5 * (xc1 + xc2), 0.5 * (yc1 + yc2))
        for i in self.items:
            x = about_object.get(i.type)[FORM]
            if x is Form.polygon:
                # для прямоугольника считаем два новых вектора
                # для точек одной диагонали
                point = self.canvas.coords(i.tag)
                new_points = new_coordinates(*center, point, alpha)
                self.canvas.coords(i.tag, new_points)
            elif x is Form.oval:
                # для круга считаем вектор – центр окружности
                point = self.canvas.coords(i.tag)
                x0 = 0.5 * (point[0] + point[2])
                y0 = 0.5 * (point[1] + point[3])
                xc, yc = vector_rotation(*center, x0, y0, alpha)
                x1 = xc - (x0 - point[0])
                y1 = yc - (y0 - point[1])
                x2 = xc + (point[2] - x0)
                y2 = yc + (point[3] - y0)
                self.canvas.coords(i.tag, [x1, y1, x2, y2])
            # проверка нарушений
            self.canvas.check_object_on_garden()
            self.canvas.check_intersection_obj()
            self.canvas.error_position()

    # строка для файла с конфигурацией
    # тип объекта и его расположение для составляющих частей
    def load_option(self):
        result = "C\n"
        for i in self.items:
            result = result + i.load_option()
        return result

    def __del__(self):
        self.list_tag.clear()
        self.items.clear()


# класс элементарный объект
class ElementaryObject:
    def __init__(self, type_obj, tag, canvas):
        self.canvas = canvas
        self.type = type_obj
        self.tag = tag
        # print("Elementary")

    # строка для файла с конфигурацией
    # тип объекта и его расположение
    def load_option(self):
        type_obj = key_by_value(dict_object, self.type)
        point = str(self.canvas.coords(self.tag))
        result = "E\n" + type_obj + "\n" + point + "\n"
        return result

    # функция движения, сдвиг на холсте в одну из сторон
    def move(self, direction):
        if direction == "l":
            self.canvas.move(self.tag, -1, 0)
        elif direction == "r":
            self.canvas.move(self.tag, 1, 0)
        elif direction == "u":
            self.canvas.move(self.tag, 0, -1)
        elif direction == "d":
            self.canvas.move(self.tag, 0, 1)
        # проверка нарушений
        self.canvas.check_object_on_garden()
        self.canvas.check_intersection_obj()
        self.canvas.error_position()

    # функция поврота
    def rotation(self, direction):
        # поворот на 5 градусов
        if direction == "l":
            alpha = -pi / 36
        elif direction == "r":
            alpha = pi / 36
        x = about_object.get(self.type)[FORM]
        # только для прямоугольных
        # вокруг центра фигуры
        # считаем два вектора
        if x is Form.polygon:
            point = self.canvas.coords(self.tag)
            center = (0.5 * (point[0] + point[4]), 0.5 * (point[1] + point[5]))
            new_points = new_coordinates(*center, point, alpha)
            self.canvas.coords(self.tag, new_points)
            self.canvas.check_object_on_garden()
            self.canvas.check_intersection_obj()
            self.canvas.error_position()


if __name__ == "__main__":
    user = UserWindow()
    user.start()
