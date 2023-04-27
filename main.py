import sys
import csv
from PyQt5.QtCore import QSize, Qt, QRect, QPoint
from PyQt5.QtGui import QPen, QPainter, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QWidget, QLineEdit, QVBoxLayout, QLabel, QFileDialog
from rectangle import Rectangle
from convexHull import ConvexHull
from filesWriter import FilesWriter


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.dots = []
        self.rect = []
        self.dots_hull = []
        self.dots_rect = []
        self.square = 0
        self.mouse = False

        self.setWindowTitle("Штука")
        self.setStyleSheet("QMainWindow {background-color: #808080;}")
        self.setFixedSize(QSize(1500, 900))

        self.dialog()

    def mousePressEvent(self, event):
        if self.mouse:
            self.dots_rect = []
            self.dots_hull = []
            self.button_file_in.setStyleSheet('''
                                    QPushButton {
                                        background-color: #808080; 
                                        color: white; 
                                        font-size: 16px; 
                                        font-weight: 600; 
                                        border-radius: 8px; 
                                    }
                                    QPushButton:hover{
                                        background-color: #999999; 
                                        color: white; 
                                        font-size: 17px; 
                                        font-weight: 600;  
                                        border-radius: 8px; 
                                    }''')
            x, y = event.x(), event.y()
            if [x - 840, -(y - 450)] not in self.dots:
                self.dots.append([x - 840, -(y - 450)])
            self.update()

    def paintEvent(self, event):
        # ширина области для рисования 1350
        painter = QPainter()
        painter.begin(self)
        self.draw_grid(painter)
        self.draw_dots(painter)
        self.draw_dots_hull(painter)
        self.draw_rect(painter)
        painter.end()

    def draw_grid(self, painter):
        painter.setPen(QPen(QColor(40, 40, 40), 2))
        painter.drawLine(150, 450, 1500, 450)
        painter.drawLine(840, 0, 840, 900)

    def draw_dots(self, painter):
        painter.setPen(QPen(QColor(100, 64, 15), 5))
        for i in range(len(self.dots)):
            painter.drawEllipse(self.dots[i][0] + 840 - 3, -self.dots[i][1] + 450 - 3, 4, 4)

    def draw_dots_hull(self, painter):
        painter.setPen(QPen(QColor(218, 165, 32), 5))
        for i in range(len(self.dots_hull)):
            painter.drawEllipse(self.dots_hull[i][0] + 840 - 3, -self.dots_hull[i][1] + 450 - 3, 4, 4)

    def draw_rect(self, painter):
        painter.setPen(QPen(QColor(119, 221, 119), 5))
        for i in range(len(self.dots_rect)):
            painter.drawLine(self.dots_rect[i - 1][0] + 840, -self.dots_rect[i - 1][1] + 450,
                             self.dots_rect[i][0] + 840, -self.dots_rect[i][1] + 450)

        painter.setPen(QPen(QColor(255, 43, 43), 5))
        for i in range(len(self.dots_rect)):
            painter.drawEllipse(self.dots_rect[i][0] + 840 - 3, -self.dots_rect[i][1] + 450 - 3, 4, 4)
            painter.drawText(self.dots_rect[i][0] + 840, -self.dots_rect[i][1] + 450 + 10,
                             f'({self.dots_rect[i][0]}, {self.dots_rect[i][1]})')
    def dialog(self):
        self.button_box = QWidget(self)
        self.button_box.resize(150, 900)
        self.button_box.move(0, 0)
        self.button_box.setStyleSheet("QWidget {background-color: #282828;}")


        self.input = QLineEdit(self)
        self.input.setPlaceholderText("Координаты")
        self.input.resize(130, 35)
        self.input.move(10, 10)
        self.input.setStyleSheet("QLineEdit {border-radius: 8px;font-size: 16px; font-weight: 600;}")

        self.button_ok = QPushButton("Ввести", self)
        self.button_ok.setCheckable(True)
        self.button_ok.resize(130, 35)
        self.button_ok.move(10, 55)
        self.button_ok.setStyleSheet('''
                QPushButton {
                    background-color: #808080; 
                    color: white; 
                    font-size: 16px; 
                    font-weight: 600; 
                    border-radius: 8px; 
                }
                QPushButton:hover{
                    background-color: #999999; 
                    color: white; 
                    font-size: 17px; 
                    font-weight: 600; 
                    border-radius: 8px; 
                }''')
        self.button_ok.clicked.connect(self.input_txt)

        self.button_file_from = QPushButton("Из файла", self)
        self.button_file_from.setCheckable(True)
        self.button_file_from.resize(130, 35)
        self.button_file_from.move(10, 145)
        self.button_file_from.setStyleSheet('''
                        QPushButton {
                            background-color: #808080; 
                            color: white; 
                            font-size: 16px; 
                            font-weight: 600; 
                            border-radius: 8px; 
                        }
                        QPushButton:hover{
                            background-color: #999999; 
                            color: white; 
                            font-size: 17px; 
                            font-weight: 600;  
                            border-radius: 8px; 
                        }''')
        self.button_file_from.clicked.connect(self.read_file)

        self.button_mouse = QPushButton("Мышка: выкл", self)
        self.button_mouse.setCheckable(True)
        self.button_mouse.resize(130, 35)
        self.button_mouse.move(10, 100)
        self.button_mouse.setStyleSheet('''
                                       QPushButton {
                                           background-color: #808080; 
                                           color: white; 
                                           font-size: 16px; 
                                           font-weight: 600; 
                                           border-radius: 8px; 
                                       }
                                       QPushButton:hover{
                                           background-color: #999999; 
                                           color: white; 
                                           font-size: 17px; 
                                           font-weight: 600;  
                                           border-radius: 8px; 
                                       }''')
        self.button_mouse.clicked.connect(self.mouse_switch)

        self.button_file_in = QPushButton("В файл", self)
        self.button_file_in.setCheckable(True)
        self.button_file_in.resize(130, 35)
        self.button_file_in.move(10, 190)
        self.button_file_in.setStyleSheet('''
                                QPushButton {
                                    background-color: #808080; 
                                    color: white; 
                                    font-size: 16px; 
                                    font-weight: 600; 
                                    border-radius: 8px; 
                                }
                                QPushButton:hover{
                                    background-color: #999999; 
                                    color: white; 
                                    font-size: 17px; 
                                    font-weight: 600;  
                                    border-radius: 8px; 
                                }''')
        self.button_file_in.clicked.connect(self.write_file)

        self.button_del = QPushButton("Очистить", self)
        self.button_del.setCheckable(True)
        self.button_del.resize(130, 35)
        self.button_del.move(10, 235)
        self.button_del.setStyleSheet('''
                        QPushButton {
                            background-color: #cc4100; 
                            color: white; 
                            font-size: 16px; 
                            font-weight: 600; 
                            border-radius: 8px; 
                        }
                        QPushButton:hover{
                            background-color: #ff5100; 
                            color: white; 
                            font-size: 17px; 
                            font-weight: 600; 
                            border-radius: 8px; 
                        }''')
        self.button_del.clicked.connect(self.clear)

        self.button_go = QPushButton("Запустить", self)
        self.button_go.setCheckable(True)
        self.button_go.resize(130, 35)
        self.button_go.move(10, 280)
        self.button_go.setStyleSheet('''
                QPushButton {
                    background-color: green; 
                    color: white; 
                    font-size: 16px; 
                    font-weight: 600; 
                    border-radius: 8px; 
                }
                QPushButton:hover{
                    background-color: #009900; 
                    color: white; 
                    font-size: 17px; 
                    font-weight: 600; 
                    border-radius: 8px; 
                }''')
        self.button_go.clicked.connect(self.go_algoritm)

        self.label = QLabel(self)
        self.label.resize(130, 35)
        self.label.move(10, 325)
        self.label.setText(f'S = {self.square}')
        self.label.setStyleSheet('''QLabel { 
                            color: #009900; 
                            font-size: 16px; 
                            font-weight: 600;  
                        }''')

    def clear(self):
        self.dots_rect = []
        self.dots = []
        self.dots_hull = []
        self.button_file_in.setStyleSheet('''
                                        QPushButton {
                                            background-color: #808080; 
                                            color: white; 
                                            font-size: 16px; 
                                            font-weight: 600; 
                                            border-radius: 8px; 
                                        }
                                        QPushButton:hover{
                                            background-color: #999999; 
                                            color: white; 
                                            font-size: 17px; 
                                            font-weight: 600;  
                                            border-radius: 8px; 
                                        }''')
        self.square = 0
        self.label.setText(f'S = {self.square}')
        self.update()


    def input_txt(self):
        self.button_file_in.setStyleSheet('''
                                QPushButton {
                                    background-color: #808080; 
                                    color: white; 
                                    font-size: 16px; 
                                    font-weight: 600; 
                                    border-radius: 8px; 
                                }
                                QPushButton:hover{
                                    background-color: #999999; 
                                    color: white; 
                                    font-size: 17px; 
                                    font-weight: 600;  
                                    border-radius: 8px; 
                                }''')
        self.dots_rect = []
        self.dots_hull = []
        text = self.input.text()
        text = text.split(',')
        lst = list()
        for i in text:
            try:
                j = int(i)
                lst.append(j)
                if len(lst) != 2:
                    continue
                if lst not in self.dots:
                    self.dots.append(lst)
                lst = list()

            except ValueError:
                continue
        self.input.setText('')
        self.update()

    def read_file(self):
        self.dots_rect = []
        self.dots_hull = []
        self.button_file_in.setStyleSheet('''
                                QPushButton {
                                    background-color: #808080; 
                                    color: white; 
                                    font-size: 16px; 
                                    font-weight: 600; 
                                    border-radius: 8px; 
                                }
                                QPushButton:hover{
                                    background-color: #999999; 
                                    color: white; 
                                    font-size: 17px; 
                                    font-weight: 600;  
                                    border-radius: 8px; 
                                }''')
        file, _ = QFileDialog.getOpenFileName(self, 'Open File', './', 'Text Files (*.csv)')
        if file:
            with open(file) as File:
                reader = csv.reader(File, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
                for i in reader:
                    if len(i) == 2:
                        lst = list()
                        try:
                            for j in i:
                                lst.append(int(j))
                        except ValueError:
                            continue
                        if lst not in self.dots:
                            self.dots.append(lst)
        self.update()

    def write_file(self):
        FilesWriter().write_csv(self.dots)
        self.button_file_in.setStyleSheet('''
                                    QPushButton {
                                        background-color: #4ed44e; 
                                        color: white; 
                                        font-size: 16px; 
                                        font-weight: 600; 
                                        border-radius: 8px; 
                                    }
                                    QPushButton:hover{
                                        background-color: #78de78; 
                                        color: white; 
                                        font-size: 17px; 
                                        font-weight: 600;  
                                        border-radius: 8px; 
                                    }''')

    def mouse_switch(self):
        if self.mouse == False:

            self.mouse = True
            self.button_mouse.setText("Мышка: вкл")
            self.button_mouse.setStyleSheet('''
                                                           QPushButton {
                                                               background-color: #214ccf; 
                                                               color: white; 
                                                               font-size: 16px; 
                                                               font-weight: 600; 
                                                               border-radius: 8px; 
                                                           }
                                                           QPushButton:hover{
                                                               background-color: #4169e1; 
                                                               color: white; 
                                                               font-size: 17px; 
                                                               font-weight: 600;  
                                                               border-radius: 8px; 
                                                           }''')
        else:
            self.mouse = False
            self.button_mouse.setText("Мышка: выкл")
            self.button_mouse.setStyleSheet('''
                                               QPushButton {
                                                   background-color: #808080; 
                                                   color: white; 
                                                   font-size: 16px; 
                                                   font-weight: 600; 
                                                   border-radius: 8px; 
                                               }
                                               QPushButton:hover{
                                                   background-color: #999999; 
                                                   color: white; 
                                                   font-size: 17px; 
                                                   font-weight: 600;  
                                                   border-radius: 8px; 
                                               }''')

    def go_algoritm(self):
        if len(self.dots) < 3:
            self.button_go.setStyleSheet('''
                                            QPushButton {
                                                background-color: #daa520; 
                                                color: white; 
                                                font-size: 16px; 
                                                font-weight: 600; 
                                                border-radius: 8px; 
                                            }
                                            QPushButton:hover{
                                                background-color: #e3b749; 
                                                color: white; 
                                                font-size: 17px; 
                                                font-weight: 600;  
                                                border-radius: 8px; 
                                            }''')
            return
        self.button_go.setText("Ждите")
        self.button_go.setStyleSheet('''QPushButton {
            background-color: #3caa3c; 
            color: white; 
            font-size: 16px; 
            font-weight: 600; 
            border-radius: 8px; }''')
        self.button_go.setEnabled(False)
        convex_hull = ConvexHull(self.dots)
        self.dots_hull = convex_hull.hull
        rect = Rectangle()
        self.dots_rect, self.square = rect.UnitUI(self.dots_hull)
        self.square = round(self.square, 1)
        # print(self.dots_rect)
        self.label.setText(f'S = {self.square}')
        # print("выполнилось")
        self.button_go.setText("Запустить")
        self.button_go.setStyleSheet('''QPushButton {
                    background-color: green; 
                    color: white; 
                    font-size: 16px; 
                    font-weight: 600; 
                    border-radius: 8px; }''')
        self.button_go.setEnabled(True)
        self.update()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    app.exec()
