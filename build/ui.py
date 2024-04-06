import tkinter as tk
from tkinter import ttk
from tkinter import Tk
from PIL import ImageTk, Image
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from utils.converters import ticks_to_time


class RowFrame(tk.Frame):
    COLOURS = {
        'Задержан': 'red',
        'Ок': 'green',
        'В процессе': 'orange'
    }

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure((0, 1), weight=1, uniform='a')
        self.columnconfigure((0, 1, 2, 3), weight=1, uniform='a')

        if data is not None:
            font = 'Inter 9'
            flight, type, status, time = data.number, data.type, data.status, data.date
            self.flight_number = tk.Label(self, text='Рейс', background='#ADADAD', font=font)
            self.flight_number_ = tk.Label(self, text=flight, background='#ADADAD', font=font)
        
            self.type = tk.Label(self, text='Тип', background='#ADADAD', font=font)
            self.type_ = tk.Label(self, text=type, background='#ADADAD', font=font)

            self.status = tk.Label(self, text='Статус', background='#ADADAD', font=font)
            self.status_ = tk.Label(self, text=status, fg=self.COLOURS[status], background='#ADADAD', font=font)

            self.time = tk.Label(self, text='Время', background='#ADADAD', font=font)
            self.time_ = tk.Label(self, text=time, background='#ADADAD', font=font)

    def grid(self, *args, **kwargs):
        super().grid(*args, **kwargs)
        self.flight_number.grid(row=0, column=0, sticky='nwse')
        self.type.grid(row=0, column=1, sticky='nwse')
        self.status.grid(row=0, column=2, sticky='nwse')
        self.time.grid(row=0, column=3, sticky='nwse')

        self.flight_number_.grid(row=1, column=0, sticky='nwse')
        self.type_.grid(row=1, column=1, sticky='nwse')
        self.status_.grid(row=1, column=2, sticky='nwse')
        self.time_.grid(row=1, column=3, sticky='nwse')
    
    def grid_forget(self, *args, **kwargs):
        self.flight_number.grid_forget()
        self.type.grid_forget()
        self.status.grid_forget()
        self.time.grid_forget()

        self.flight_number_.grid_forget()
        self.type_.grid_forget()
        self.status_.grid_forget()
        self.time_.grid_forget()
        super().grid_forget(*args, **kwargs)


class PageFrame(tk.Frame):
    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.rowconfigure((0, 1, 2), weight=1, uniform='b')
        self.columnconfigure(0, weight=1, uniform='b')
        self.rows = [RowFrame(master=self, data=data[idx], background='green') for idx in range(len(data))]
    
    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        for idx, row in enumerate(self.rows):
            row.grid(column=0, row=idx, padx=5, pady=10)

    def place_forget(self, *args, **kwargs):
        for idx, row in enumerate(self.rows):
            row.grid_forget()
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


class StatsFrame(BoxFrame):
    def __init__(self, runways, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._items = ('Среднее отклонение', 'Очереди')
        self._value = tk.StringVar(value=self._items[1])
        self.runways = runways
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
        self.stats['queue'] = self.get_queue_stats_widget()
    
    def combobox_handler(self, *args):
        match self._value.get():
            case 'Очереди':
                plt.close()
                self.stats['Очереди'].place_forget()
                self.stats['Очереди'] = self.get_queue_stats_widget()
                self.stats['Очереди'].place(width=274, height=219, x=41, y=93)

    def place_stats(self):
        match self._value.get():
            case 'Очереди':
                self.stats['Очереди'] = self.get_queue_stats_widget()
                self.stats['Очереди'].place(width=274, height=219, x=41, y=93)

    def place_stats_forget(self):
        plt.close()
        match self._value.get():
            case 'Очереди':
                self.stats['Очереди'].place_forget()

    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.combobox.place(x=198, y=16, width=139, height=37)
        self.place_stats()
    
    def place_forget(self, *args, **kwargs):
        plt.close()
        self.combobox.place_forget()
        self.place_stats_forget()
        super().place_forget(*args, **kwargs)
    
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
        pass


class FlightBoardFrame(BoxFrame):
    DATA = [
        ('S-01', 'Взлет', 'Задержан', '19:20'),
        ('S-02', 'Взлет', 'Задержан', '19:35'),
        ('S-03', 'Посадка', 'Ок', '19:37'),
        ('S-04', 'Посадка', 'Задержан', '19:40'),
        ('S-05', 'Взлет', 'В процессе', '19:42'),
        ('S-06', 'Посадка', 'В процессе', '19:51'),
        ('S-07', 'Посадка', 'В процессе', '19:52'),
    ]
    MAX_PAGES = len(DATA) // 3 + int(len(DATA) % 3 != 0)

    def __init__(self, data, *args, **kwargs):
        super().__init__(*args, **kwargs)
        FlightBoardFrame.DATA = data
        FlightBoardFrame.MAX_PAGES = len(self.DATA) // 3 + int(len(self.DATA) % 3 != 0)
        self.page_idx = 0
        self.page = PageFrame(data=self.DATA[3 * self.page_idx : 3 * self.page_idx + 3], master=self, background='#C7C4C4')
        self.image_forward = tk.PhotoImage(file='build/assets/next.png')
        self.image_backward = tk.PhotoImage(file='build/assets/back.png')
        self.next = tk.Button(self, image=self.image_forward, command=self._next, background='#C7C4C4')
        self.prev = tk.Button(self, image=self.image_backward, command=self._prev, background='#C7C4C4')
    
    def _next(self):
        if self.page_idx == self.MAX_PAGES - 1:
            return

        self.page.place_forget()
        self.page_idx += 1
        self.page = PageFrame(
            data=self.DATA[3 * self.page_idx : 3 * self.page_idx + 3],
            master=self,
            background='#C7C4C4'
        )
        self.page.place(width=274, height=219, x=41, y=89)
    
    def _prev(self):
        if self.page_idx == 0:
            return

        self.page.place_forget()
        self.page_idx -= 1
        self.page = PageFrame(
            data=self.DATA[3 * self.page_idx : 3 * self.page_idx + 3],
            master=self,
            background='#C7C4C4'
        )
        self.page.place(width=274, height=219, x=41, y=89)
    
    def place(self, *args, **kwargs):
        super().place(*args, **kwargs)
        self.page.place(width=274, height=219, x=41, y=89)
        self.prev.place(x=147, y=322)
        self.next.place(x=177, y=322)


class GUI(Tk):
    def __init__(self, title, size, background, experiment, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title(title)
        self.geometry(f'{size[0]}x{size[1]}')
        self['background'] = background
        self.experiment = experiment
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
            runways=self.experiment.handler.runways,
            title='Статистика',
            background='#C7C4C4'
        )
        self.box_left = FlightBoardFrame(
            master=self,
            data=self.experiment.flight_board,
            title='Расписание',
            background='#C7C4C4'
        )
        self.button_img = ImageTk.PhotoImage(Image.open('build/assets/frame0/button_1.png'))
        self.make = tk.Button(
            self,
            image=self.button_img,
            background='#D9D9D9',
            command=self.tick
        )
        self.make_label = tk.Label(self.make, text='Сделать шаг', font='Regular 7')

    def tick(self):
        plt.close()
        self.experiment()
        self.time_var.set(ticks_to_time(self.experiment.ticks))
        self.box_right.place_stats_forget()
        self.box_right.place_stats()

    def on_exit(self):
        plt.close()
        self.destroy()

    def run(self):
        self.top_frame.place(x=0, y=0, width=960, height=85)
        self.label.place(x=79, y=0)
        self.title.place(x=180, y=21)
        self.time.place(x=739, y=21, width=138, height=47)
        self.box_right.place(x=66, y=127, width=356, height=356)
        self.box_left.place(x=538, y=127, width=356, height=356)
        self.make.place(x=413, y=486)
        self.make_label.place(x=35, y=10)

        self.mainloop()
