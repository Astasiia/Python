from tkinter import *
from tkinter.ttk import Combobox
from PIL import Image, ImageTk
from constants import *
from help_function import key_by_value, new_point


# загрузка изображений для кнопок, размер задается
def load_image(name, size):
    image = Image.open(name)
    image = image.resize((size, size))
    return image


# расположение на фрейме 4 кнопок
def four_button_place(lst_btn, lbl):
    lbl.place(x=20, y=20)
    lst_btn[0].place(x=20, y=60, width=120, height=50)
    lst_btn[1].place(x=20, y=130, width=120, height=50)
    lst_btn[2].place(x=150, y=60, width=120, height=50)
    lst_btn[3].place(x=150, y=130, width=120, height=50)


# функции для создания виджетов для их расположения на основном окне
# создание кнопок для движения и поврота объектов
def create_btn_move(window):
    # разобраться с функцией, не работает при вызове функции вместо кода
    work_move_obj = Frame(window, width=320, height=160, bg="lightgray")
    work_move_obj.place(x=290, y=430)
    # imageR = Image.open("right.png")
    # imageR = imageR.resize((35, 35))
    image_r = load_image("right.png")
    image_r = ImageTk.PhotoImage(image_r)
    image_l = load_image("left.png")
    image_l = ImageTk.PhotoImage(image_l)
    image_u = load_image("up.png")
    image_u = ImageTk.PhotoImage(image_u)
    image_d = load_image("down.png")
    image_d = ImageTk.PhotoImage(image_d)
    btn_left = Button(work_move_obj, width=35, height=35, image=image_l,
                      command=lambda: window.canvas.move_obj("l"))
    btn_right = Button(work_move_obj, width=35, height=35, image=image_r,
                       command=lambda: window.canvas.move_obj("r"))
    btn_up = Button(work_move_obj, width=35, height=35, image=image_u,
                    command=lambda: window.canvas.move_obj("u"))
    btn_down = Button(work_move_obj, width=35, height=35, image=image_d,
                      command=lambda: window.canvas.move_obj("d"))
    # lbl_rotation = Label(work_move_obj,
    #                      text="Поворот",
    #                      font=("Times New Roman", 18),
    #                      bg="lightgray")
    # btn_ok = Button(work_move_obj,
    #                 text="OK",
    #                 font=("Times New Roman", 18),
    #                 command=lambda: set_select(None, self.canvas))
    # var_rot = IntVar()
    # var_rot.set(0)
    # input_rot = Spinbox(work_move_obj, from_=0, to=360, textvariable=var_rot)
    btn_left.place(x=20, y=60)
    btn_right.place(x=100, y=60)
    btn_up.place(x=60, y=20)
    btn_down.place(x=60, y=100)
    # lbl_rotation.place(x=180, y=20)
    # input_rot.place(x=185, y=60, width=70)
    # btn_ok.place(x=200, y=100, width=40, height=40)


# создание кнопок для работы с объектами
def create_btn_obj(window):
    work_obj = Frame(window, width=290, height=200, bg="lightyellow",
                     bd=5, relief=RIDGE)
    work_obj.place(x=0, y=550)
    lbl = Label(work_obj,
                text="Управление объектами холста",
                font=("Times New Roman", 18),
                bg="lightyellow")
    btn_merge = Button(work_obj,
                       text="Объединить",
                       font=("Times New Roman", 18),
                       fg="blue",
                       command=lambda: window.canvas.merge())
    btn_split = Button(work_obj,
                       text="Разъединить",
                       font=("Times New Roman", 18),
                       fg="blue",
                       command=lambda: window.canvas.separation())
    btn_delete = Button(work_obj,
                        text="Удалить",
                        font=("Times New Roman", 18),
                        fg="blue",
                        command=lambda: window.canvas.delete_obj())
    btn_clear = Button(work_obj,
                       text="Очистить",
                       font=("Times New Roman", 18),
                       fg="blue",
                       command=window.canvas.clear)
    four_button_place([btn_merge, btn_split, btn_delete, btn_clear], lbl)


# кнопки для работы с проектом
def create_btn_prj(window):
    work_prj = Frame(window, width=290, height=340, bg="lightyellow",
                     bd=5, relief=RIDGE)
    work_prj.place(x=700, y=0)
    lbl = Label(work_prj,
                text="Управление проектом",
                font=("Times New Roman", 18),
                bg="lightyellow")
    btn_exit = Button(work_prj,
                      text="Выход",
                      font=("Times New Roman", 18),
                      fg="red",
                      command=window.close)
    btn_save = Button(work_prj,
                      text="Сохранить",
                      font=("Times New Roman", 18),
                      fg="red",
                      command=window.save_config)
    btn_load = Button(work_prj,
                      text="Загрузить",
                      font=("Times New Roman", 18),
                      fg="red",
                      command=window.download)
    btn_picture = Button(work_prj,
                         text="Рисунок",
                         font=("Times New Roman", 18),
                         fg="red",
                         command=window.save_picture)
    btn_list_object = Button(work_prj,
                             text="Список объектов",
                             font=("Times New Roman", 18),
                             fg="red",
                             command=window.canvas.information)
    btn_instruction = Button(work_prj,
                             text="Инструкция",
                             font=("Times New Roman", 18),
                             fg="red",
                             command=window.instruction)
    four_button_place([btn_exit, btn_save, btn_load, btn_picture], lbl)
    btn_list_object.place(x=20, y=200, width=250, height=50)
    btn_instruction.place(x=20, y=270, width=250, height=50)


# кнопки для задания участка для расположения на холсте
def create_btn_garden(window):
    work_garden = Frame(window, width=290, height=210, bg="lightyellow",
                        bd=5, relief=RIDGE)
    work_garden.place(x=700, y=340)
    lbl = Label(work_garden,
                text="Задание участка",
                font=("Times New Roman", 18),
                bg="lightyellow")
    lbl_x = Label(work_garden,
                  text="X, м",
                  font=("Times New Roman", 18),
                  bg="lightyellow")
    lbl_y = Label(work_garden,
                  text="Y, м",
                  font=("Times New Roman", 18),
                  bg="lightyellow")
    lbl_coverage = Label(work_garden,
                         text="Покрытие",
                         font=("Times New Roman", 18),
                         bg="lightyellow")
    btn_garden = Button(work_garden,
                        text="Создать",
                        font=("Times New Roman", 18))
    var_x = IntVar()
    var_x.set(30)
    var_y = IntVar()
    var_y.set(20)
    input_x = Spinbox(work_garden, from_=0, to=60, textvariable=var_x)
    input_y = Spinbox(work_garden, from_=0, to=45, textvariable=var_y)
    input_coverage = Combobox(work_garden)
    input_coverage["values"] = list_coverage
    input_coverage.current(0)
    lbl.place(x=20, y=20)
    lbl_coverage.place(x=20, y=100)
    input_coverage.place(x=110, y=100, width=140)
    lbl_x.place(x=20, y=60)
    input_x.place(x=70, y=60, width=60)
    lbl_y.place(x=140, y=60)
    input_y.place(x=190, y=60, width=60)
    btn_garden.place(x=80, y=140, width=120, height=50)
    btn_garden['command'] = lambda: window.canvas.create_garden(input_x, input_y, input_coverage)


# кнопки добавления новых объектов на холст
def create_btn_add(window):
    work_add = Frame(window, width=290, height=200, bg="lightyellow",
                     bd=5, relief=RIDGE)
    work_add.place(x=700, y=550)
    lbl = Label(work_add,
                text="Добавление нового объекта",
                font=("Times New Roman", 18),
                bg="lightyellow")
    btn_plant = Button(work_add,
                       text="Растение",
                       font=("Times New Roman", 18),
                       fg="green",
                       command=lambda: window.canvas.select_new_obj(list_plant))
    btn_coverage = Button(work_add,
                          text="Покрытие",
                          font=("Times New Roman", 18),
                          fg="green",
                          command=lambda: window.canvas.select_new_obj(list_coverage))
    btn_build = Button(work_add,
                       text="Здание",
                       font=("Times New Roman", 18),
                       fg="green",
                       command=lambda: window.canvas.select_new_obj(list_build))
    btn_furniture = Button(work_add,
                           text="Мебель",
                           font=("Times New Roman", 18),
                           fg="green",
                           command=lambda: window.canvas.select_new_obj(list_furniture))
    four_button_place([btn_plant, btn_coverage, btn_build, btn_furniture], lbl)


def create_btn_function(window):
    function = Frame(window, width=160, height=200, bg="lightyellow",
                     bd=5, relief=RIDGE)
    function.place(x=540, y=550)
    lbl = Label(function,
                text="Функции",
                font=("Times New Roman", 18),
                bg="lightyellow")
    btn_distance = Button(function,
                          text="Расстояние",
                          font=("Times New Roman", 18),
                          fg="black",
                          command=window.canvas.distance)
    btn_drop = Button(function,
                      text="Отмена",
                      font=("Times New Roman", 18),
                      fg="black",
                      command=window.canvas.drop)
    lbl.place(x=20, y=20)
    btn_distance.place(x=20, y=60, width=120, height=50)
    btn_drop.place(x=20, y=130, width=120, height=50)


# создание нового окна для выбора добавляемого объекта
def create_window_select(window, list_obj):
    new_window = Toplevel()
    new_window.grab_set()
    new_window.title("Новый объект")
    new_window.geometry('300x200')
    lbl_obj = Label(new_window,
                    text="Выберете объект",
                    font=("Times New Roman", 18))
    lbl_obj.place(x=20, y=20)
    obj = Combobox(new_window)
    obj['values'] = list_obj
    obj.current(0)
    obj.place(x=20, y=50, width=260)
    btn_yes = Button(new_window,
                     text="Добавить",
                     font=("Times New Roman", 18),
                     command=lambda: window.canvas.draw_object(obj, new_window))
    btn_no = Button(new_window,
                    text="Отмена",
                    font=("Times New Roman", 18),
                    command=new_window.destroy)
    btn_yes.place(x=20, y=180, width=120, height=50, anchor="sw")
    btn_no.place(x=280, y=180, width=120, height=50, anchor="se")


# создание окна с информацией об объектах
def create_info(count):
    new_window = Toplevel()
    new_window.grab_set()
    new_window.title("Информация")
    new_window.geometry('400x400')
    scroll_y = Scrollbar(new_window, orient=VERTICAL,
                         troughcolor="red")
    canvas = Canvas(new_window, width=350, height=400,
                    yscrollcommand=scroll_y.set)
    scroll_y.config(command=canvas.yview)
    canvas.pack()
    scroll_y.place(x=400, y=0, anchor="ne", height=400)
    elem = about_object.keys()
    x = 170
    y = 50
    for i in elem:
        info = about_object.get(i)
        point = new_point(info[POINT], x, y)
        color = info[COLOR]
        form = info[FORM]
        if form is Form.polygon:
            canvas.create_polygon(point, fill=color, outline=color)
            dy = point[5] - point[1]
        elif form is Form.oval:
            canvas.create_oval(point, fill=color, outline=color)
            dy = point[3] - point[1]
        name = key_by_value(dict_object, i)
        count_name = str(count.get(i))
        text = name + ": " + count_name + " шт."
        canvas.create_text(100, y + 5, text=text, font="TimesNewRoman")
        dy = max(dy, 15)
        y = y + dy + 10
