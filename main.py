from enum import Enum
from tkinter import *
from tkinter.messagebox import *
from tkinter import filedialog
from tkinter.ttk import Combobox
from PIL import Image, ImageTk


FORM = 0
COLOR = 1


select_object = None
select_comb = []
number = 0


# Coverage = Enum('Coverage', 'grass, asphalt, tiles')
TypeObject = Enum('TypeObject', 'table, chair, bench,'
                                'summerhouse, bathhouse, house,'
                                'tiles, asphalt, grass,'
                                'flower, bush, tree')
Color = Enum('Color', 'red, green, blue, yellow')
Form = Enum('Form', 'polygon, oval')
Select = Enum('Select', 'one, no_one')

select_flag = Select.one

# Списки возможных объектов по типу объекта
list_furniture = ["стол", "стул", "лавочка"]
list_build = ["беседка", "баня", "дом"]
list_coverage = ["плитка", "асфальт", "трава"]
list_plant = ["цветок", "куст", "дерево"]


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


# dict_object = {"стол": (TypeObject.table, Form.polygon, "brown"),
#                "стул": (TypeObject.chair, Form.oval, "brown"),
#                "лавочка": (TypeObject.bench, Form.polygon, "yellow"),
#                "беседка": (TypeObject.summerhouse, Form.oval, "black"),
#                "баня": (TypeObject.bathhouse, Form.polygon, "black"),
#                "дом": (TypeObject.house, Form.polygon, "black"),
#                "плитка": (TypeObject.tiles, Form.polygon, "gray"),
#                "асфальт": (TypeObject.asphalt, Form.polygon, "black"),
#                "трава": (TypeObject.grass, Form.polygon, "green"),
#                "цветок": (TypeObject.flower, Form.polygon, "red"),
#                "куст": (TypeObject.bush, Form.polygon, "green"),
#                "дерево": (TypeObject.tree, Form.polygon, "green")}


def combining(canvas):
    global select_flag, select_object, select_comb
    if select_flag == Select.one:
        select_flag = Select.no_one
        if select_object is not None:
            select_comb.append(select_object)
    else:
        for i in range(0, len(select_comb)):
            color = canvas.itemcget(select_comb[i], "fill")
            canvas.itemconfig(select_comb[i], outline=color)
        canvas.combining_obj(select_comb)
        select_comb.clear()
        select_flag = Select.one


def separation(canvas):
    global select_object
    if select_object is None:
        return
    x = canvas.all_obj.get(select_object)
    if x == "e":
        return
    else:
        canvas.item_config_all(select_object, None)
        canvas.separation_obj(select_object)


def load_image(name):
    image = Image.open(name)
    image = image.resize((35, 35))
    return image


def set_select(obj, canvas):
    global select_object
    if select_flag == Select.one:
        if select_object is not None:
            x = canvas.all_obj.get(select_object)
            if x == "e":
                color = canvas.itemcget(select_object, "fill")
                canvas.itemconfig(select_object, outline=color)
            else:
                canvas.item_config_all(select_object, None)
        if obj is select_object:
            select_object = None
            return
        select_object = obj
    else:
        x = select_comb.count(obj)
        if x:
            x = select_comb.index(obj)
            select_comb.pop(x)
            color = canvas.itemcget(obj, "fill")
            canvas.itemconfig(obj, outline=color)
            select_object = None
            return
        else:
            select_comb.append(obj)
    x = canvas.all_obj.get(obj)
    if x == "e":
        canvas.itemconfig(obj, outline="green2")
    else:
        canvas.item_config_all(obj, "green2")


def new_object(obj, canvas, window):
    type_obj = dict_object.get(obj.get())
    a = canvas.create_oval(0, 0, 30, 30, fill="red", outline="red", activeoutline="cyan", width=5)
    canvas.tag_bind(a, '<Button-1>', lambda event: set_select(a, canvas))
    canvas.add_elementary(type_obj, a)
    window.destroy()


def new_window(list_obj, canvas):
    window = Toplevel()
    window.title("Новый объект")
    window.geometry('300x300')
    lbl_obj = Label(window,
                    text="Выберете объект",
                    font=("Times New Roman", 18))
    lbl_obj.place(x=20, y=20)
    obj = Combobox(window)
    obj['values'] = list_obj
    obj.current(0)
    obj.place(x=20, y=50, width=260)
    btn_yes = Button(window,
                     text="Добавить",
                     font=("Times New Roman", 18),
                     command=lambda: new_object(obj, canvas, window))
    btn_no = Button(window,
                    text="Отмена",
                    font=("Times New Roman", 18),
                    command=window.destroy)
    btn_yes.place(x=20, y=280, width=120, height=50, anchor="sw")
    btn_no.place(x=280, y=280, width=120, height=50, anchor="se")


def msg_exit(window):
    ans = askyesno("Выход", "Перед выходом сохраните файл!\n Вы действительноо хотите выйти?")
    if ans:
        window.destroy()


def msg_save(canvas):
    filetypes = [("TXT", "*.txt")]
    new_file = filedialog.asksaveasfilename(filetypes=filetypes)
    if new_file:
        f = open(new_file, 'w')
        # canvas.save_config(f)
        f.close()


def msg_load(canvas):
    filetypes = [("TXT", "*.txt")]
    file = filedialog.askopenfilename(filetypes=filetypes)
    if file:
        f = open(file, 'r')
        canvas.download(f)
        f.close


def aaa(canv, a, x, y):
    canv.move(a, x, y)


def move_one(r, canvas, obj):
    if r == "l":
        canvas.move(obj, -5, 0)
    elif r == "r":
        canvas.move(obj, 5, 0)
    elif r == "u":
        canvas.move(obj, 0, -5)
    elif r == "d":
        canvas.move(obj, 0, 5)


def move_all(r, canvas):
    global select_object
    for i in canvas.list_combining:
        if select_object in i.list_tag:
            break
    for j in i.list_tag:
        move_one(r, canvas, j)


def move_obj(r, canvas):
    global select_object
    if select_object is None:
        return
    x = canvas.all_obj.get(select_object)
    if x == "e":
        move_one(r, canvas, select_object)
    else:
        move_all(r, canvas)


def create_garden(canvas, in_x, in_y, in_coverage):
    x = 10*int(in_x.get())
    y = 10*int(in_y.get())
    x0 = 300 - int(x/2)
    y0 = 200 - int(y/2)
    canvas.delete(canvas.garden)
    canvas.garden = canvas.create_polygon((x0, y0), (x0+x, y0), (x0+x, y0+y), (x0, y0+y),
                                          outline="black", fill="green")
    canvas.tag_lower(canvas.garden)
    canvas.set_vertical(y)
    canvas.set_horizontal(x)
    coverage = dict_object.get(in_coverage.get())
    canvas.change_coverage(coverage)


def create_btn_move(window):
    work_move_obj = Frame(window, width=320, height=160, bg="lightgray")
    work_move_obj.place(x=290, y=430)
    imageR = Image.open("right.png")
    imageR = imageR.resize((35, 35))
    imageR = ImageTk.PhotoImage(imageR)
    imageL = Image.open("left.png")
    imageL = imageL.resize((35, 35))
    imageL = ImageTk.PhotoImage(imageL)
    imageU = Image.open("up.png")
    imageU = imageU.resize((35, 35))
    imageU = ImageTk.PhotoImage(imageU)
    imageD = Image.open("down.png")
    imageD = imageD.resize((35, 35))
    imageD = ImageTk.PhotoImage(imageD)
    btn_left = Button(work_move_obj, width=35, height=35, image=imageL,
                      command=lambda: move_obj("l", window.canvas))
    btn_right = Button(work_move_obj, width=35, height=35, image=imageR,
                       command=lambda: move_obj("r", window.canvas))
    btn_up = Button(work_move_obj, width=35, height=35, image=imageU,
                    command=lambda: move_obj("u", window.canvas))
    btn_down = Button(work_move_obj, width=35, height=35, image=imageD,
                      command=lambda: move_obj("d", window.canvas))
    lbl_rotation = Label(work_move_obj,
                         text="Поворот",
                         font=("Times New Roman", 18),
                         bg="lightgray")
    btn_ok = Button(work_move_obj,
                    text="OK",
                    font=("Times New Roman", 18))
    var_rot = IntVar()
    var_rot.set(0)
    input_rot = Spinbox(work_move_obj, from_=0, to=360, textvariable=var_rot)
    btn_left.place(x=20, y=60)
    btn_right.place(x=100, y=60)
    btn_up.place(x=60, y=20)
    btn_down.place(x=60, y=100)
    lbl_rotation.place(x=180, y=20)
    input_rot.place(x=185, y=60, width=70)
    btn_ok.place(x=200, y=100, width=40, height=40)


def create_btn_obj(window):
    work_obj = Frame(window, width=290, height=160, bg="lightgrey")
    work_obj.place(x=0, y=430)
    btn_merge = Button(work_obj,
                       text="Объединить",
                       font=("Times New Roman", 18),
                       fg="blue",
                       command=lambda: combining(window.canvas))
    btn_split = Button(work_obj,
                       text="Разъединить",
                       font=("Times New Roman", 18),
                       fg="blue",
                       command=lambda: separation(window.canvas))
    btn_delete = Button(work_obj,
                        text="Удалить",
                        font=("Times New Roman", 18),
                        fg="blue",
                        command=lambda: window.canvas.del_obj(select_object))
    btn_clear = Button(work_obj,
                       text="Очистить",
                       font=("Times New Roman", 18),
                       fg="blue",
                       command=window.canvas.clear)
    btn_merge.place(x=20, y=20, width=120, height=50)
    btn_split.place(x=20, y=90, width=120, height=50)
    btn_delete.place(x=150, y=20, width=120, height=50)
    btn_clear.place(x=150, y=90, width=120, height=50)


def create_btn_prj(window):
    work_prj = Frame(window, width=160, height=230, bg="lightgray")
    work_prj.place(x=900, y=0, anchor="ne")
    btn_exit = Button(work_prj,
                      text="Выход",
                      font=("Times New Roman", 18),
                      fg="red",
                      command=lambda: msg_exit(window))
    btn_save = Button(work_prj,
                      text="Сохранить",
                      font=("Times New Roman", 18),
                      fg="red",
                      command=lambda: msg_save(window.canvas))
    btn_load = Button(work_prj,
                      text="Загрузить",
                      font=("Times New Roman", 18),
                      fg="red",
                      command=lambda: msg_load(window.canvas))
    btn_exit.place(x=20, y=20, width=120, height=50)
    btn_save.place(x=20, y=90, width=120, height=50)
    btn_load.place(x=20, y=160, width=120, height=50)


def create_btn_garden(window):
    work_garden = Frame(window, width=270, height=200, bg="lightgray")
    lbl_x = Label(work_garden,
                  text="X",
                  font=("Times New Roman", 18),
                  bg="lightgray")
    lbl_y = Label(work_garden,
                  text="Y",
                  font=("Times New Roman", 18),
                  bg="lightgray")
    lbl_coverage = Label(work_garden,
                         text="Покрытие",
                         font=("Times New Roman", 18),
                         bg="lightgray")
    btn_garden = Button(work_garden,
                        text="Создать",
                        font=("Times New Roman", 18))
    var_x = IntVar()
    var_x.set(30)
    var_y = IntVar()
    var_y.set(20)
    input_x = Spinbox(work_garden, from_=0, to=60, textvariable=var_x)
    input_y = Spinbox(work_garden, from_=0, to=40, textvariable=var_y)
    input_coverage = Combobox(work_garden)
    input_coverage["values"] = list_coverage
    input_coverage.current(0)
    lbl_coverage.place(x=20, y=20)
    input_coverage.place(x=110, y=20, width=120)
    lbl_x.place(x=20, y=60)
    input_x.place(x=50, y=60, width=70)
    lbl_y.place(x=130, y=60)
    input_y.place(x=160, y=60, width=70)
    btn_garden.place(x=70, y=100, width=120, height=50)
    work_garden.place(x=900, y=430, anchor="se")
    btn_garden['command'] = lambda: create_garden(window.canvas, input_x, input_y, input_coverage)


def create_btn_add(window):
    work_add = Frame(window, width=290, height=160, bg="lightgray")
    work_add.place(x=900, y=430, anchor="ne")
    btn_plant = Button(work_add,
                       text="Растение",
                       font=("Times New Roman", 18),
                       fg="green",
                       command=lambda: new_window(list_plant, window.canvas))
    btn_coverage = Button(work_add,
                          text="Покрытие",
                          font=("Times New Roman", 18),
                          fg="green",
                          command=lambda: new_window(list_coverage, window.canvas))
    btn_build = Button(work_add,
                       text="Здание",
                       font=("Times New Roman", 18),
                       fg="green",
                       command=lambda: new_window(list_build, window.canvas))
    btn_furniture = Button(work_add,
                           text="Мебель",
                           font=("Times New Roman", 18),
                           fg="green",
                           command=lambda: new_window(list_furniture, window.canvas))
    btn_plant.place(x=20, y=20, width=120, height=50)
    btn_coverage.place(x=20, y=90, width=120, height=50)
    btn_build.place(x=150, y=20, width=120, height=50)
    btn_furniture.place(x=150, y=90, width=120, height=50)
    # btn_furniture['command'] = lambda: canvas.add_elementary(TypeObject.table)


class UserWindow(Tk):
    def __init__(self):
        super().__init__()
        self.title("Создай свой участок")
        self.geometry('900x600')
        self["bg"] = "lightgray"
        self.canvas = WorkingField(self)

    def create_button(self):
        create_btn_obj(self)
        create_btn_prj(self)
        create_btn_add(self)
        create_btn_garden(self)
        # create_btn_move(self)

    def start(self):
        self.create_button()
        work_move_obj = Frame(self, width=320, height=160, bg="lightgray")
        work_move_obj.place(x=290, y=430)
        imageR = Image.open("right.png")
        imageR = imageR.resize((35, 35))
        imageR = ImageTk.PhotoImage(imageR)
        imageL = Image.open("left.png")
        imageL = imageL.resize((35, 35))
        imageL = ImageTk.PhotoImage(imageL)
        imageU = Image.open("up.png")
        imageU = imageU.resize((35, 35))
        imageU = ImageTk.PhotoImage(imageU)
        imageD = Image.open("down.png")
        imageD = imageD.resize((35, 35))
        imageD = ImageTk.PhotoImage(imageD)
        btn_left = Button(work_move_obj, width=35, height=35, image=imageL,
                          command=lambda: move_obj("l", self.canvas))
        btn_right = Button(work_move_obj, width=35, height=35, image=imageR,
                           command=lambda: move_obj("r", self.canvas))
        btn_up = Button(work_move_obj, width=35, height=35, image=imageU,
                        command=lambda: move_obj("u", self.canvas))
        btn_down = Button(work_move_obj, width=35, height=35, image=imageD,
                          command=lambda: move_obj("d", self.canvas))
        lbl_rotation = Label(work_move_obj,
                             text="Поворот",
                             font=("Times New Roman", 18),
                             bg="lightgray")
        # btn_ok = Button(work_move_obj,
        #                 text="OK",
        #                 font=("Times New Roman", 18),
        #                 command=lambda: set_select(None, self.canvas))
        var_rot = IntVar()
        var_rot.set(0)
        input_rot = Spinbox(work_move_obj, from_=0, to=360, textvariable=var_rot)
        btn_left.place(x=20, y=60)
        btn_right.place(x=100, y=60)
        btn_up.place(x=60, y=20)
        btn_down.place(x=60, y=100)
        lbl_rotation.place(x=180, y=20)
        input_rot.place(x=185, y=60, width=70)
        # btn_ok.place(x=200, y=100, width=40, height=40)
        self.mainloop()


class WorkingField(Canvas):
    def __init__(self, window):
        super().__init__(window, width=600, height=400, bg="white")
        self.place(x=20, y=20)
        self.garden = None
        self.list_elementary = []
        self.list_combining = []
        self.all_obj = {}
        self.vertical_len = 0
        self.horizontal_len = 0
        self.coverage = None

    def get_vertical(self):
        return self.vertical_len

    def get_horizontal(self):
        return self.horizontal_len

    def set_vertical(self, new_vertical):
        self.vertical_len = new_vertical

    def set_horizontal(self, new_horizontal):
        self.horizontal_len = new_horizontal

    def add_elementary(self, type_obj, tag):
        x = ElementaryObject(type_obj, tag)
        self.list_elementary.append(x)
        self.all_obj.update({tag: "e"})

    def add_compound(self, list_item):
        x = CompoundObject(list_item)
        self.list_combining.append(x)
        for i in list_item:
            self.all_obj.update({i.tag: "c"})

    def del_obj(self, obj):
        x = self.all_obj.get(obj)
        if x == "e":
            self.delete(obj)
            for i in self.list_elementary:
                if obj == i.tag:
                    self.list_elementary.remove(i)
                    break
        else:
            for i in self.list_combining:
                if obj in i.list_tag:
                    break
            for j in i.list_tag:
                self.delete(j)
            self.list_combining.remove(i)

    def clear(self):
        self.delete(ALL)
        self.list_elementary.clear()
        self.list_combining.clear()

    def change_coverage(self, new_coverage):
        self.coverage = new_coverage

    def check_intersection(self):
        pass

    def combining_obj(self, list_comb):
        list_item = []
        for i in self.list_elementary:
            if i.tag in list_comb:
                list_item.append(i)
        for i in list_item:
            self.list_elementary.remove(i)
        self.add_compound(list_item)

    def separation_obj(self, obj):
        for i in self.list_combining:
            if obj in i.list_tag:
                break
        self.list_combining.remove(i)
        self.list_elementary.extend(i.items)
        for j in i.items:
            self.all_obj.update({j.tag: "e"})


    def distance(self):
        pass

    def save_config(self, file):
        file.write("AAA\n")

    def download(self, file):
        pass

    def save_image(self):
        pass

    def close(self):
        pass

    def item_config_all(self, obj, color):
        for i in self.list_combining:
            if obj in i.list_tag:
                break
        if color is None:
            for j in i.list_tag:
                color0 = self.itemcget(j, "fill")
                self.itemconfig(j, outline=color0)
        else:
            for j in i.list_tag:
                self.itemconfig(j, outline=color)



class GraphicObject:
    def __init__(self):
        self.x = 20
        self.y = 20
        self.rot = 0

    def change_coordinate(self, delta_x, delta_y):
        self.x = self.x + delta_x
        self.y = self.y + delta_y

    def change_rotation(self, delta_rot):
        self.rot = self.rot + delta_rot

    def change_attributes(self, new_list_attr):
        pass

    def get_location(self):
        pass


class CompoundObject():
    def __init__(self, list_item):
        self.items = list_item
        self.list_tag = []
        for i in list_item:
            self.list_tag.append(i.tag)
        print("Compound")

    def add_item(self, coordinate):
        pass

    def del_item(self):
        pass

    def get_size(self):
        pass


class ElementaryObject():
    def __init__(self, type_obj, tag):
        self.type = type_obj
        self.tag = tag
        # canvas.create_polygon
        print("Elementary")

    def get_size(self):
        pass


user = UserWindow()
user.start()
