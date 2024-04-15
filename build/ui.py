import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils.converters import ticks_to_time
from common.structs.airport import Experiment
from collections import namedtuple


class RowFrame(tk.Frame):
    def __init__(self, data, font, width=274, height=73, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = height
        self.width = width
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1, uniform='a')
        self.columnconfigure(1, weight=1, uniform='a')
        self.columnconfigure(2, weight=1, uniform='a')
        self.columnconfigure(3, weight=3, uniform='a')
        flight_number, type, status, time = data.number, data.type, data.status, data.date
        self.flight_number = tk.Label(self, text=flight_number, background='#BDBABA', font=font)
        self.type = tk.Label(self, text=type, background='#BDBABA', font=font)
        self.status = tk.Label(self, text=status, background='#BDBABA', font=font)
        self.time = tk.Label(self, text=time, background='#BDBABA', font=font)

    def place(self, *args, **kwargs):
        super().place(*args, width=self.width, height=self.height, **kwargs)
        self.flight_number.grid(row=0, column=0, sticky='nsew')
        self.time.grid(row=0, column=1, sticky='nsew')
        self.type.grid(row=0, column=2, sticky='nsew')
        self.status.grid(row=0, column=3, sticky='nsew')

    def place_forget(self, *args, **kwargs):
        self.flight_number.grid_forget()
        self.type.grid_forget()
        self.status.grid_forget()
        self.time.grid_forget()
        super().place_forget(*args, **kwargs)


class PageFrame(tk.Frame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure((0, 1, 2), weight=1)
        self.columnconfigure(0, weight=1)
        self.headers = RowFrame(
            master=self,
            data=namedtuple('data', ('number', 'type', 'status', 'date'))('Рейс', 'Тип', 'Статус', 'Время'),
            height=24,
            font='Inter 8 bold',
            background='#BDBABA'
        )
        self.rows = [RowFrame(master=self, data=data[idx], height=39, font='Inter 8', background='#BDBABA') for idx in range(len(data))]
    
    def place(self, *args, **kwargs):
        super().place(*args, width=274, height=220, **kwargs)
        self.headers.place(x=0, y=0)
        for idx, row in enumerate(self.rows):
            row.place(x=0, y=self.headers.height + row.height * idx)
    
    def place_forget(self, *args, **kwargs):
        for row in self.rows:
            row.place_forget()
        self.headers.place_forget()
        super().place_forget(*args, **kwargs)


class BoxFrame(tk.Frame):
    def __init__(self, title='box title', *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.top_frame = tk.Frame(self, background='#FFFFFF')
        self.top_label = tk.Label(self.top_frame, text=title, background='#FFFFFF', font='Inter 10 bold')
    
    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.top_frame.place(relx=0, rely=0, width=356, height=67)
        self.top_label.place(width=101, height=20, x=37, y=24)


class StatsRow(tk.Frame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = [(tk.Label(self, text=d[0], font='Inter 8', background='#BDBABA'), tk.Label(self, text=d[1], font='Inter 8', background='#BDBABA')) for d in data]
        self.rowconfigure(tuple(range(len(data))), weight=1)
        self.columnconfigure((0, 1), weight=1)

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        for row, d in enumerate(self.data):
            d[0].grid(row=row, column=0)
            d[1].grid(row=row, column=1)

    def place_forget(self, *args, **kwargs):
        for d in self.data[::-1]:
            d[0].grid_forget()
            d[1].grid_forget()
        super().place_forget(*args, **kwargs)


class StatsFrame(BoxFrame):
    def __init__(self, experiment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items = ('Численная статистика', 'Очереди')
        self._value = tk.StringVar(value=self._items[1])
        self.runways = experiment.handler.runways
        self.statistics = experiment.stats
        self.combobox= ttk.Combobox(
            self.top_frame,
            textvariable=self._value,
            values=self._items,
            background='#E8E3E3',
            font='Regular 7',
            state="readonly",
            justify='center'
        )
        self.combobox.bind('<<ComboboxSelected>>', self.combobox_handler)
        self.stats = {}

    def get_widget(self):
        value = self._value.get()
        # print(value)
        match value:
            case 'Очереди':
                self.stats[value] = self.get_queue_stats_widget()
            case 'Численная статистика':
                self.stats[value] = self.get_delay_stats_widget()

    def get_queue_stats_widget(self):
        fig = plt.figure(figsize=(2.5, 2.2), facecolor='#C7C4C4')
        ax = fig.add_subplot()
        ax.set_title('Состояние очередей')
        ax.set_xticks(range(1, len(self.runways) + 1))
        ax.set_yticks(range(1, 8))
        plt.ylim(0,7)
        x = list(range(1, len(self.runways) + 1))
        y = [len(runway) for runway in self.runways]
        plt.bar(x, y, color='#000000')
        canvas = FigureCanvasTkAgg(figure=fig, master=self)
        return canvas.get_tk_widget()

    def get_delay_stats_widget(self):
        data = [(key.value, value[-1] if value else 0) for key, value in self.statistics.items()]
        return StatsRow(master=self, data=data, background='#BDBABA')        

    def combobox_handler(self, _):
        self.place_stats()

    def place_stats(self):
        plt.close('all')
        self.get_widget()
        self.stats[self._value.get()].place(width=274, height=219, x=41, y=93)

    def place_stats_forget(self):
        value = self._value.get()
        self.stats[value].place_forget()

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.combobox.place(x=198, y=16, width=139, height=37)
        self.place_stats()

    def place_forget(self, *args, **kwargs):
        self.place_stats_forget()
        self.combobox.place_forget()
        super().place_forget(*args, **kwargs)


class FlightBoardFrame(BoxFrame):
    PAGE_SIZE = 5

    def __init__(self, experiment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = experiment.flight_board
        self.max_pages = len(self.data) // self.PAGE_SIZE + int(len(self.data) % self.PAGE_SIZE != 0)
        self.page_idx = 0
        self.page = PageFrame(data=self.data[self.PAGE_SIZE * self.page_idx : self.PAGE_SIZE * self.page_idx + self.PAGE_SIZE], master=self, background='#C7C4C4')
        self.image_forward = tk.PhotoImage(file='build/assets/next.png')
        self.image_backward = tk.PhotoImage(file='build/assets/back.png')
        self.next = tk.Button(self, image=self.image_forward, command=self._next, background='#C7C4C4')
        self.prev = tk.Button(self, image=self.image_backward, command=self._prev, background='#C7C4C4')
    
    def _next(self):
        if self.page_idx == self.max_pages - 1:
            return
        self.page_idx += 1
        self.place_forget()
        self.place(x=538, y=127, width=356, height=356)
    
    def _prev(self):
        if self.page_idx == 0:
            return
        self.page_idx -= 1
        self.place_forget()
        self.place(x=538, y=127, width=356, height=356)
    
    def update_page(self):
        self.page = PageFrame(
            data=self.data[self.PAGE_SIZE * self.page_idx : self.PAGE_SIZE * self.page_idx + self.PAGE_SIZE],
            master=self,
            background='#C7C4C4'
        )

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.update_page()
        self.page.place(x=41, y=89)
        self.prev.place(x=147, y=322)
        self.next.place(x=177, y=322)


class GUI(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title('Program')
        self.geometry('950x540')
        self['background'] = '#E3E1E1'
        self.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.top_frame = tk.Frame(self, background='#999999')
        self.img = ImageTk.PhotoImage(Image.open("build/assets/frame0/image_4.png"))
        self.label = tk.Label(
            self.top_frame,
            image=self.img,
            background='#999999'
        )
        self.title = tk.Label(
            self.top_frame,
            text='Flight Radar',
            font='Regular 24 bold',
            background='#999999'
        )
        self.init_frame = tk.Frame(self, background='#C7C4C4')
        self.n_runways_value = tk.StringVar(self, value='Кол-во полос')
        self.n_runways = tk.Entry(self.init_frame, textvariable=self.n_runways_value, justify='center', font='Inter 8')
        self.n_runways_flag = True
        self.n_runways.bind("<Button-1>", self.delete_runways_text)
        self.step_value = tk.StringVar(self, value='Шаг моделирования (мин)')
        self.step = tk.Entry(self.init_frame, textvariable=self.step_value, justify='center', font='Inter 6')
        self.step_flag = True
        self.step.bind("<Button-1>", self.delete_step_text)
        self.apply_button = tk.Button(self.init_frame, text='Применить', command=self.apply, font='Inter 8')
        self.image_restart = tk.PhotoImage(file='build/assets/restart.png')
        self.restart_button = tk.Button(self, image=self.image_restart, command=self.restart)
        self.image_rewind = tk.PhotoImage(file='build/assets/rewind.png')
        self.rewind_button = tk.Button(self, image=self.image_rewind, command=self.rewind)
        self.make = tk.Button(
            self,
            text='Сделать шаг',
            background='#D9D9D9',
            command=self.tick
        )

    def rewind(self):
        self.rewind_button['state'] = 'disabled'
        self.tick(force=True)

    def delete_runways_text(self, _):
        if self.n_runways_flag:
            self.n_runways.delete(0, tk.END)
            self.n_runways_flag = False

    def delete_step_text(self, _):
        if self.step_flag:
            self.step.delete(0, tk.END)
            self.step_flag = False

    def apply(self):
        self.experiment = Experiment(n_runways=int(self.n_runways_value.get()), step=int(self.step_value.get()))
        self.time_var = tk.IntVar(self, value=ticks_to_time(self.experiment.ticks))
        self.time = tk.Label(
            self.top_frame,
            text=self.time_var,
            textvariable=self.time_var,
            background='#C4BFBF',
            font='Inter 16 bold',
            anchor='center'
        )
        self.box_right = StatsFrame(
            master=self,
            experiment=self.experiment,
            title='Статистика',
            background='#C7C4C4'
        )
        self.box_left = FlightBoardFrame(
            master=self,
            experiment=self.experiment,
            title='Расписание',
            background='#C7C4C4'  
        )
        self._place_init_forget()
        self._place()

    def tick(self, force=False):
        self.experiment(force)
        self.time_var.set(ticks_to_time(self.experiment.ticks))
        self.box_right.place_stats()
        self.box_left.place(x=538, y=127, width=356, height=356)
        if self.experiment.over:
            self.make['state'] = self.rewind_button['state'] = 'disabled' 

    def on_exit(self):
        plt.close('all')
        self.destroy()

    def restart(self):
        self.make['state'] = self.rewind_button['state'] = 'active'
        self.n_runways_flag = True
        self.step_flag = True
        self.n_runways_value.set('Кол-во полос')
        self.step_value.set('Шаг моделирования (мин)')
        self._place_forget()
        self._place_init()

    def run(self):
        self._place_init()
        self.mainloop()

    def _place_init(self):
        self.top_frame.place(x=0, y=0, width=960, height=85)
        self.label.place(x=79, y=0)
        self.title.place(x=180, y=21)
        self.init_frame.place(relx=0.5, rely=0.5, width=274, height=220, anchor='center')
        self.n_runways.place(width=135, height=28, x=73, y=60)
        self.step.place(width=135, height=28, x=73, y=110)
        self.apply_button.place(width=75, height=28, x=103, y=171)

    def _place_init_forget(self):
        self.init_frame.place_forget()
        self.n_runways.place_forget()
        self.step.place_forget()
        self.apply_button.place_forget()

    def _place(self):
        self.time.place(x=739, y=21, width=138, height=47)
        self.box_right.place(x=66, y=127, width=356, height=356)
        self.box_left.place(x=538, y=127, width=356, height=356)
        self.make.place(x=421, y=486)
        self.restart_button.place(x=874, y=486, width=20, height=20)
        self.rewind_button.place(x=854, y=486, width=20, height=20)

    def _place_forget(self):
        self.time.place_forget()
        self.box_right.place_forget()
        self.box_left.place_forget()
        self.make.place_forget()
        self.restart_button.place_forget()
        self.rewind_button.place_forget()
