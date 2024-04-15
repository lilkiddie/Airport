from build.ui import GUI


class App:
    def __init__(self):
        self.ui = GUI()
        self.ui.run()

app = App()