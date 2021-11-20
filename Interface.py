import random
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import numpy as np
import sys
import SocketReceiver



class Window(QMainWindow):

    def __init__(self, image_files):
        super().__init__()
        self.image_files = image_files
        sf = "Slides are shown {} seconds apart"
        self.label = QLabel(self)
        self.s = SocketReceiver.SocketReceiver()
        self.setWindowTitle(sf.format(4000 / 1000.0))
        self.flag = False
        self.LikeButton = QPushButton(self)
        self.DislikeButton = QPushButton(self)
        self.NeutralButton = QPushButton(self)
        self.ScaleButton1 = QPushButton(self)
        self.ScaleButton2 = QPushButton(self)
        # self.Start_test = QPushButton(self)
        self.setStyleSheet("background-color: black;")
        self.index = random.randint(0, len(self.image_files) - 1)
        self.setGeometry(0, 0, 1300, 1000)
        self.showMaximized()
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.second_event)
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.change)
        print("HERE \n")
        self.show()

    def beginEx(self):
        self.s.connect('127.0.0.1', 54123)
        print("bsssss1")
        self.change()

    def change(self):
        self.randomizer()
        self.s.start_record()
        self.timer2.stop()
        try:
            if len(self.image_files) == 0:
                self.finish()
                return
            self.label.clear()
            self.label.clear()
            self.LikeButton.hide()
            self.DislikeButton.hide()
            self.NeutralButton.hide()
            self.ScaleButton1.hide()
            self.ScaleButton2.hide()
            # self.Start_test.hide()
            file = self.image_files[self.index]
            image = QPixmap('images/' + str(file) + '.jpg')
            if image.width() > 1950 or image.height() > 1050:
                image = image.scaled(1950, 1050)
                self.label.move(0, 0)
            elif image.width() < 1950 / 3 and image.height() < 1050 / 3:
                image = image.scaled(1950 / 3, 1050 / 3)
                self.label.move((1950 - image.width()) // 2, (1050 - image.height()) // 2)
            else:
                self.label.move((1950 - image.width()) // 2, (1050 - image.height()) // 2)
            self.label.setScaledContents(True)
            self.label.setPixmap(image)
            self.label.resize(image.width(), image.height())
            self.label.show()
            self.timer1.start(4000)
        except Exception as ex:
            print("change \n", ex)
        # self.second_event()

    def randomizer(self):
        if self.flag:
            try:
                self.image_files = np.delete(self.image_files, self.index)
                self.index = random.randint(0, len(self.image_files) - 1)
            except Exception as ex:
                print("random \n", ex)
        else:
            self.flag = True

    def black_screen(self, text):
        print("STUCK")
        self.label.clear()
        self.LikeButton.hide()
        self.DislikeButton.hide()
        self.NeutralButton.hide()
        self.ScaleButton1.hide()
        self.ScaleButton2.hide()
        self.setStyleSheet("background-color: black;")
        # change here
        file1 = open('labels/thirdtry/islam/' + str(self.image_files[self.index]) + '.txt', "w")
        file1.write(text)
        file1.close()
        print(self.image_files)
        self.timer2.start(1000)

    def second_event(self):
        data = self.s.end_record()
        print("Ss")
        self.timer1.stop()
        my_string = ""
        for entry in data:
            for my_input in entry:
                my_string += str(my_input) + "\t"
            my_string += "\n"
        # change here
        file1 = open('data/islam3/islam_' + str(self.image_files[self.index]) + '.txt', "w")
        file1.write(str(my_string))
        file1.close()
        # print(my_string)
        self.label.clear()
        self.LikeButton.show()
        self.DislikeButton.show()
        self.NeutralButton.show()
        self.ScaleButton1.show()
        self.ScaleButton2.show()
        self.setStyleSheet("background-color: black;")
        self.LikeButton.setText("Like")  # text
        self.LikeButton.setStyleSheet("background-color: green;")
        self.LikeButton.setShortcut('Ctrl+L')  # shortcut key
        self.LikeButton.clicked.connect(lambda: self.black_screen('one'))
        self.LikeButton.setGeometry(0, 0, 300, 100)
        self.LikeButton.move(100, 500)

        self.ScaleButton1.setText("Somehow Like")  # text
        self.ScaleButton1.setStyleSheet("background-color: lime;")
        self.ScaleButton1.setShortcut('Ctrl+N')  # shortcut key
        self.ScaleButton1.clicked.connect(lambda: self.black_screen("two"))
        self.ScaleButton1.setGeometry(0, 0, 300, 100)
        self.ScaleButton1.move(450, 500)

        self.NeutralButton.setText("Neutral")  # text
        self.NeutralButton.setStyleSheet("background-color: yellow;")
        self.NeutralButton.setShortcut('Ctrl+N')  # shortcut key
        self.NeutralButton.clicked.connect(lambda: self.black_screen("three"))
        self.NeutralButton.setGeometry(0, 0, 300, 100)
        self.NeutralButton.move(800, 500)

        self.ScaleButton2.setText("Somehow Dislike")  # text
        self.ScaleButton2.setStyleSheet("background-color: orange;")
        self.ScaleButton2.setShortcut('Ctrl+N')  # shortcut key
        self.ScaleButton2.clicked.connect(lambda: self.black_screen("four"))
        self.ScaleButton2.setGeometry(0, 0, 300, 100)
        self.ScaleButton2.move(1150, 500)

        self.DislikeButton.setText("Dislike")  # tex
        self.DislikeButton.setStyleSheet("background-color: red;")
        self.DislikeButton.setShortcut('Ctrl+D')  # shortcut key
        self.DislikeButton.clicked.connect(lambda: self.black_screen("five"))
        self.DislikeButton.setGeometry(0, 0, 300, 100)
        self.DislikeButton.move(1500, 500)
        print('b455555')

    def finish(self):
        self.label.clear()
        self.setStyleSheet("background-color: black;")
        self.label.move(0, 0)
        self.LikeButton.hide()
        self.DislikeButton.hide()
        self.NeutralButton.hide()
            # self.Start_test.show()
        # self.Start_test.setText("Start Testing")  # text
        # self.Start_test.setStyleSheet("background-color: green;")
        # self.Start_test.setShortcut('Ctrl+N')  # shortcut key
        # self.Start_test.clicked.connect(lambda: self.start_life_test())
        image = QPixmap('images/thank_you.jpg')
        image = image.scaled(1950, 1050)
        self.label.setScaledContents(True)
        self.label.setPixmap(image)
        self.label.resize(image.width(), image.height())
        self.label.show()
        # self.NeutralButton.setGeometry(0, 0, 300, 100)
        # self.NeutralButton.move(800, 500)


App = QApplication(sys.argv)
images = np.array([i + 1 for i in range(80)])
window = Window(images)
window.beginEx()

sys.exit(App.exec())
