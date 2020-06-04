import kivy.app
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.dropdown import DropDown
import datetime
import random
import math
import pdb

class Perceptron:
    def __init__(self, threshold: int, dot_list: list, learning_rate: float, 
                 deadline: float, deadline_type: str):
        self.w1 = 0
        self.w2 = 0
        self.P = threshold
        self.dots = dot_list
        self.delta = learning_rate
        self.iteration = 0
        
        if deadline_type == 'time':
            self.deadline = datetime.timedelta(seconds=deadline)
            self.deadline_type = deadline_type
        elif deadline_type == 'iterations':
            self.deadline = deadline
            self.deadline_type = deadline_type
        else:
            raise Exception('Deadline_type should be "time" or "iterations", ' + \
                            'not "{}".'.format(deadline_type))

    def __repr__(self):
        return """Perceptron(w1={}, w2={}, P={}, dots={}, delta={},
               deadline=({}, {}))""".format(self.w1, self.w2, self.P, self.dots,
                        self.delta, self.deadline_type, self.deadline)

    def train(self):
        if self.deadline_type == 'time':
            now = datetime.datetime.now()
            end = now + self.deadline
        else:
            now = 0
            end = self.deadline

        dot_ind = 0
        while now < end:
            self.iteration += 1  # updating iterations
            curr_rez, dot_ind = self.step(dot_ind)

            if curr_rez and prev_rez:
                break
            prev_rez = curr_rez
            now = datetime.datetime.now() if self.deadline_type == 'time' else now + 1

    def step(self, dot_ind):
        dot = self.dots[dot_ind]
        y = self.w1 * dot[0] + self.w2 * dot[1]
            
        if dot_ind == 0 and y < self.P:
            diff = self.P - y
            self.w1 = self.w1 + diff * dot[0] * self.delta
            self.w2 = self.w2 + diff * dot[1] * self.delta
            dot_ind = (dot_ind + 1) % 2
            return False, dot_ind

        elif dot_ind == 1 and y > self.P:
            diff = y - self.P
            self.w1 = self.w1 + diff * dot[0] * self.delta
            self.w2 = self.w2 + diff * dot[1] * self.delta 
            dot_ind = (dot_ind + 1) % 2
            return False, dot_ind

        else:
            dot_ind = (dot_ind + 1) % 2
            return True, dot_ind



class SimpleApp(kivy.app.App):
    def build(self): 
        self.label = Label(text="Choose parameters for the perceptron.")
        
        self.label_P = Label(text="Write your threshold:")
        self.input_P = TextInput() 
        
        self.label_1dot = Label(text="Write coordinates for first dot:")
        self.input_1dot = TextInput()
        self.label_2dot = Label(text="Write coordinates for second dot:")
        self.input_2dot = TextInput()

        self.label_d = Label(text="Write your learning rate:")
        self.input_d = TextInput()

        self.label_type = Label(text="Choose the type of deadline:")
        self.dropdown = DropDown()
        self.drop_btn1 = Button(text='time', size_hint_y=None, height=44)
        self.drop_btn1.bind(on_release=lambda btn: self.dropdown.select(self.drop_btn1.text))
        self.dropdown.add_widget(self.drop_btn1)
        self.drop_btn2 = Button(text='iterations', size_hint_y=None, height=44)
        self.drop_btn2.bind(on_release=lambda btn: self.dropdown.select(self.drop_btn2.text))
        self.dropdown.add_widget(self.drop_btn2)

        self.dropbtn = Button(text="Choose here", size_hint=(None, None))
        self.dropbtn.bind(on_release=self.dropdown.open)
        self.dropdown.bind(on_select=lambda instance, x: setattr(self.dropbtn, 'text', x))

        self.label_deadline = Label(text="Write deadline in seconds/iterations.")
        self.input_deadline = TextInput()

        self.button = Button(text="Start training")
        self.button.bind(on_press=self.displayMessage)

        self.boxLayout = kivy.uix.boxlayout.BoxLayout(orientation="vertical")
        self.boxLayout.add_widget(self.label)
        self.boxLayout.add_widget(self.label_P)
        self.boxLayout.add_widget(self.input_P)
        self.boxLayout.add_widget(self.label_1dot)
        self.boxLayout.add_widget(self.input_1dot)
        self.boxLayout.add_widget(self.label_2dot)
        self.boxLayout.add_widget(self.input_2dot)
        self.boxLayout.add_widget(self.label_d)
        self.boxLayout.add_widget(self.input_d)
        self.boxLayout.add_widget(self.label_type)
        self.boxLayout.add_widget(self.dropbtn)
        self.boxLayout.add_widget(self.label_deadline)
        self.boxLayout.add_widget(self.input_deadline)
        self.boxLayout.add_widget(self.button)

        return self.boxLayout

    def displayMessage(self, btn):
        try:
            threshold = int(self.input_P.text)
            dot1 = [float(self.input_1dot.text.split(" ")[0]), float(self.input_2dot.text.split(" ")[1])]
            dot2 = [float(self.input_2dot.text.split(" ")[0]), float(self.input_2dot.text.split(" ")[1])]
            dot_list = [dot1, dot2]
            learning_rate = float(self.input_d.text)
            deadline_type = getattr(self.dropbtn, 'text')
            deadline = float(self.input_deadline.text)

            perc = Perceptron(threshold=threshold, dot_list=dot_list, learning_rate=learning_rate, deadline=deadline, deadline_type=deadline_type)
            perc.train()
            self.label.text = repr(perc)

            popup = Popup(title='# of iterations', content=Label(text=str()))
            popup.open()

        except Exception:
            self.label.text = "Wrong arguments were given. Check all of them"


if __name__ == "__main__":
    app = SimpleApp()
    app.run()

    #all_dots = [(0, 6), (1, 5), (3, 3), (2, 4)]
    #dots = random.sample(all_dots, 2)
    #lr = random.choice([0.001, 0.01, 0.05, 0.1, 0.2, 0.3])
    #time_deadlines = random.choice([0.5, 1, 2, 5])
    #iter_deadlines = random.choice([100, 200, 500, 1000])

    #perc = Perceptron(threshold=4, dot_list=dots, learning_rate=lr,
    #                  deadline=iter_deadlines, deadline_type='iterations')
