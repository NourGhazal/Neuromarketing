import pickle
import random
import statistics

import scipy.signal
import pandas as pd
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import numpy as np

import SocketReceiver
import pywt
import sys


class TestWindow(QMainWindow):
    def __init__(self, image_files):
        super().__init__()
        self.image_files = image_files
        sf = "Slides are shown {} seconds apart"
        self.label = QLabel(self)
        self.s = SocketReceiver.SocketReceiver()
        self.setWindowTitle(sf.format(4000 / 1000.0))
        self.flag = False
        self.setStyleSheet("background-color: black;")
        self.index = random.randint(0, len(self.image_files) - 1)
        self.setGeometry(0, 0, 1300, 1000)
        self.showMaximized()
        self.timer1 = QtCore.QTimer()
        self.timer1.timeout.connect(self.second_event)
        self.timer2 = QtCore.QTimer()
        self.timer2.timeout.connect(self.change)
        self.NextButton = QPushButton(self)
        self.NextButton2 = QPushButton(self)

        print("HERE \n")
        self.show()

    def beginEx(self):
        self.s.connect('127.0.0.1', 54123)
        print("bsssss1")
        self.change()

    def change(self):
        self.randomizer()
        self.setWindowTitle(str(self.image_files[self.index]))
        self.s.start_record()
        self.timer2.stop()
        self.NextButton.hide()
        self.NextButton2.hide()
        try:
            if len(self.image_files) == 0:
                self.finish()
                return
            self.label.clear()
            self.label.clear()
            try:
                file = self.image_files[self.index]
                print(file)
                image = QPixmap('images_test/' + str(file) + '.jpg')
            except Exception as e:
                print(e)
            if image.width() > 1950 and image.height() > 1050:
                image = image.scaled(1950, 1050)
                self.label.move(0, 0)
            elif image.width() > 1950:
                image = image.scaled(1950, image.height())
            elif image.height() > 1050:
                image = image.scaled(image.width(), 1050)
            elif image.width() < 1950 / 3 and image.height() < 1050 / 3:
                image = image.scaled(1950 // 3, 1050 // 3)
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

    def black_screen(self):
        try:
            print("STUCK")
            self.label.clear()
            self.NextButton.hide()
            self.NextButton2.hide()
            self.setStyleSheet("background-color: black;")
            # change here
        except Exception as ex:
            # print(self.image_files)
            print(ex)
        print("HERE")
        self.timer2.start(1000)

    def second_event(self):
        # TODO: change from reading file to recording
        try:

            data = self.s.end_record()
            print("Ss")
            self.timer1.stop()
            self.label.clear()
            self.NextButton2.hide()
            self.setStyleSheet("background-color: black;")
            print(data)
            gamma_data1 = {
                "1stgamma": [],
                "2ndgamma": [],
                "3rdgamma": [],
                "12thgamma": [],
                "13thgamma": [],
                "14thgamma": []
            }
            beta_data1 = {
                "1stbeta": [],
                "2ndbeta": [],
                "3rdbeta": [],
                "12thbeta": [],
                "13thbeta": [],
                "14thbeta": []
            }
            alpha_data1 = {
                "1stalpha": [],
                "2ndalpha": [],
                "3rdalpha": [],
                "12thalpha": [],
                "13thalpha": [],
                "14thalpha": []
            }
            theta_data1 = {
                "1sttheta": [],
                "2ndtheta": [],
                "3rdtheta": [],
                "12ththeta": [],
                "13ththeta": [],
                "14ththeta": []
            }
            delta_data1 = {
                "1stdelta": [],
                "2nddelta": [],
                "3rddelta": [],
                "12thdelta": [],
                "13thdelta": [],
                "14thdelta": []
            }
            user_data = {
                '1st': [],
                '2nd': [],
                '3rd': [],
                '12th': [],
                '13th': [],
                '14th': []
            }
            for entry in data:
                user_data['1st'].append(float(entry[0]))
                user_data['2nd'].append(float(entry[1]))
                user_data['3rd'].append(float(entry[2]))
                user_data['12th'].append(float(entry[11]))
                user_data['13th'].append(float(entry[12]))
                user_data['14th'].append(float(entry[13]))
            my_string = ""
            for entry in data:
                for my_input in entry:
                    my_string += str(my_input) + "\t"
                my_string += "\n"
                # change here
            file1 = open('data/islam3/islamtest_' + str(self.image_files[self.index]) + '.txt', "w")
            file1.write(str(my_string))
            file1.close()
            # f = open("E:/GUC/S08/GUI/data/youssef/youssef48.txt", "r")
            # string = f.read()
            # my = string.split('\n')
            # for electrode in my:
            #     ny = electrode.split('\t')
            #     if ny[0] == '':
            #         break
            #     user_data['1st'].append(float(ny[0]))
            #     user_data['2nd'].append(float(ny[1]))
            #     user_data['3rd'].append(float(ny[2]))
            #     user_data['12th'].append(float(ny[11]))
            #     user_data['13th'].append(float(ny[12]))
            #     user_data['14th'].append(float(ny[13]))
            #     print(user_data)

            user_data = pd.DataFrame.from_dict(user_data)
            first_electrode = user_data['1st']
            second_electrode = user_data['2nd']
            third_electrode = user_data['3rd']
            twelveth_electrode = user_data['12th']
            thirteenth_electrode = user_data['13th']
            fouteenth_electrode = user_data['14th']

            user_data.apply(lambda row: self.carf(row), axis=1)
            # print(user_data.head())
            s_golay_filtered_signal1 = scipy.signal.savgol_filter(first_electrode, 5, 2)
            s_golay_filtered_signal2 = scipy.signal.savgol_filter(second_electrode, 5, 2)
            s_golay_filtered_signal3 = scipy.signal.savgol_filter(third_electrode, 5, 2)
            s_golay_filtered_signal12 = scipy.signal.savgol_filter(twelveth_electrode, 5, 2)
            s_golay_filtered_signal13 = scipy.signal.savgol_filter(thirteenth_electrode, 5, 2)
            s_golay_filtered_signal14 = scipy.signal.savgol_filter(fouteenth_electrode, 5, 2)

            cA1, d11 = pywt.dwt(s_golay_filtered_signal1, 'db4')
            cA12, d12 = pywt.dwt(cA1, 'db4')
            cA13, d13 = pywt.dwt(cA12, 'db4')
            a14, d14 = pywt.dwt(cA13, 'db4')
            gamma_RMS1 = np.sqrt(sum([d11[i] ** 2 for i in range(d11.size)]) / d11.size)
            beta_RMS1 = np.sqrt(sum([d12[i] ** 2 for i in range(d12.size)]) / d12.size)
            alpha_RMS1 = np.sqrt(sum([d13[i] ** 2 for i in range(d13.size)]) / d13.size)
            theta_RMS1 = np.sqrt(sum([d14[i] ** 2 for i in range(d14.size)]) / d14.size)
            delta_RMS1 = np.sqrt(sum([a14[i] ** 2 for i in range(a14.size)]) / a14.size)
            gamma_data1['1stgamma'].append(gamma_RMS1)
            beta_data1['1stbeta'].append(beta_RMS1)
            alpha_data1['1stalpha'].append(alpha_RMS1)
            theta_data1['1sttheta'].append(theta_RMS1)
            delta_data1['1stdelta'].append(delta_RMS1)

            cA2, d21 = pywt.dwt(s_golay_filtered_signal2, 'db4')
            cA22, d22 = pywt.dwt(cA2, 'db4')
            cA23, d23 = pywt.dwt(cA22, 'db4')
            a24, d24 = pywt.dwt(cA23, 'db4')
            gamma_RMS2 = np.sqrt(sum([d21[i] ** 2 for i in range(d21.size)]) / d21.size)
            beta_RMS2 = np.sqrt(sum([d22[i] ** 2 for i in range(d22.size)]) / d22.size)
            alpha_RMS2 = np.sqrt(sum([d23[i] ** 2 for i in range(d23.size)]) / d23.size)
            theta_RMS2 = np.sqrt(sum([d24[i] ** 2 for i in range(d24.size)]) / d24.size)
            delta_RMS2 = np.sqrt(sum([a24[i] ** 2 for i in range(a24.size)]) / a24.size)
            gamma_data1['2ndgamma'].append(gamma_RMS2)
            beta_data1['2ndbeta'].append(beta_RMS2)
            alpha_data1['2ndalpha'].append(alpha_RMS2)
            theta_data1['2ndtheta'].append(theta_RMS2)
            delta_data1['2nddelta'].append(delta_RMS2)

            cA3, d31 = pywt.dwt(s_golay_filtered_signal3, 'db4')
            cA32, d32 = pywt.dwt(cA3, 'db4')
            cA33, d33 = pywt.dwt(cA32, 'db4')
            a34, d34 = pywt.dwt(cA33, 'db4')
            gamma_RMS3 = np.sqrt(sum([d31[i] ** 2 for i in range(d31.size)]) / d31.size)
            beta_RMS3 = np.sqrt(sum([d32[i] ** 2 for i in range(d32.size)]) / d32.size)
            alpha_RMS3 = np.sqrt(sum([d33[i] ** 2 for i in range(d33.size)]) / d33.size)
            theta_RMS3 = np.sqrt(sum([d34[i] ** 2 for i in range(d34.size)]) / d34.size)
            delta_RMS3 = np.sqrt(sum([a34[i] ** 2 for i in range(a34.size)]) / a34.size)
            gamma_data1['3rdgamma'].append(gamma_RMS3)
            beta_data1['3rdbeta'].append(beta_RMS3)
            alpha_data1['3rdalpha'].append(alpha_RMS3)
            theta_data1['3rdtheta'].append(theta_RMS3)
            delta_data1['3rddelta'].append(delta_RMS3)

            cA12, d121 = pywt.dwt(s_golay_filtered_signal12, 'db4')
            cA122, d122 = pywt.dwt(cA12, 'db4')
            cA123, d123 = pywt.dwt(cA122, 'db4')
            a124, d124 = pywt.dwt(cA123, 'db4')
            gamma_RMS12 = np.sqrt(sum([d121[i] ** 2 for i in range(d121.size)]) / d11.size)
            beta_RMS12 = np.sqrt(sum([d122[i] ** 2 for i in range(d122.size)]) / d12.size)
            alpha_RMS12 = np.sqrt(sum([d123[i] ** 2 for i in range(d123.size)]) / d13.size)
            theta_RMS12 = np.sqrt(sum([d124[i] ** 2 for i in range(d124.size)]) / d14.size)
            delta_RMS12 = np.sqrt(sum([a124[i] ** 2 for i in range(a124.size)]) / a14.size)
            gamma_data1['12thgamma'].append(gamma_RMS12)
            beta_data1['12thbeta'].append(beta_RMS12)
            alpha_data1['12thalpha'].append(alpha_RMS12)
            theta_data1['12ththeta'].append(theta_RMS12)
            delta_data1['12thdelta'].append(delta_RMS12)

            cA13, d131 = pywt.dwt(s_golay_filtered_signal13, 'db4')
            cA132, d132 = pywt.dwt(cA13, 'db4')
            cA133, d133 = pywt.dwt(cA132, 'db4')
            a134, d134 = pywt.dwt(cA133, 'db4')
            gamma_RMS13 = np.sqrt(sum([d131[i] ** 2 for i in range(d131.size)]) / d11.size)
            beta_RMS13 = np.sqrt(sum([d132[i] ** 2 for i in range(d132.size)]) / d12.size)
            alpha_RMS13 = np.sqrt(sum([d133[i] ** 2 for i in range(d133.size)]) / d13.size)
            theta_RMS13 = np.sqrt(sum([d134[i] ** 2 for i in range(d134.size)]) / d14.size)
            delta_RMS13 = np.sqrt(sum([a134[i] ** 2 for i in range(a134.size)]) / a14.size)
            gamma_data1['13thgamma'].append(gamma_RMS13)
            beta_data1['13thbeta'].append(beta_RMS13)
            alpha_data1['13thalpha'].append(alpha_RMS13)
            theta_data1['13ththeta'].append(theta_RMS13)
            delta_data1['13thdelta'].append(delta_RMS13)

            cA14, d141 = pywt.dwt(s_golay_filtered_signal14, 'db4')
            cA142, d142 = pywt.dwt(cA14, 'db4')
            cA143, d143 = pywt.dwt(cA142, 'db4')
            a144, d144 = pywt.dwt(cA143, 'db4')
            gamma_RMS14 = np.sqrt(sum([d141[i] ** 2 for i in range(d141.size)]) / d141.size)
            beta_RMS14 = np.sqrt(sum([d142[i] ** 2 for i in range(d142.size)]) / d142.size)
            alpha_RMS14 = np.sqrt(sum([d143[i] ** 2 for i in range(d143.size)]) / d143.size)
            theta_RMS14 = np.sqrt(sum([d144[i] ** 2 for i in range(d144.size)]) / d144.size)
            delta_RMS14 = np.sqrt(sum([a144[i] ** 2 for i in range(a144.size)]) / a144.size)
            gamma_data1['14thgamma'].append(gamma_RMS14)
            beta_data1['14thbeta'].append(beta_RMS14)
            alpha_data1['14thalpha'].append(alpha_RMS14)
            theta_data1['14ththeta'].append(theta_RMS14)
            delta_data1['14thdelta'].append(delta_RMS14)

            gamma_data1 = pd.DataFrame.from_dict(gamma_data1)
            beta_data1 = pd.DataFrame.from_dict(beta_data1)
            alpha_data1 = pd.DataFrame.from_dict(alpha_data1)
            theta_data1 = pd.DataFrame.from_dict(theta_data1)
            delta_data1 = pd.DataFrame.from_dict(delta_data1)
            merged = {**gamma_data1, **beta_data1, **alpha_data1, **theta_data1, **delta_data1}
            merged = pd.DataFrame.from_dict(merged)

            with open("E:/GUC/S08/neuromarketing dataset/Data-EEG-25-users-Neuromarketing/trees/islam_tree.pkl",
                      'rb') as my_input:
                dtree1 = pickle.load(my_input)
                dtree2 = pickle.load(my_input)
                dtree3 = pickle.load(my_input)
                dtree4 = pickle.load(my_input)
                dtree5 = pickle.load(my_input)
                dtree6 = pickle.load(my_input)
                pca_gamma = pickle.load(my_input)
                pca_beta = pickle.load(my_input)
                pca_alpha = pickle.load(my_input)
                pca_theta = pickle.load(my_input)
                pca_delta = pickle.load(my_input)
                pca_merged = pickle.load(my_input)
                gamma_standardizing = pickle.load(my_input)
                beta_standardizing = pickle.load(my_input)
                alpha_standardizing = pickle.load(my_input)
                theta_standardizing = pickle.load(my_input)
                delta_standardizing = pickle.load(my_input)
                merged_standardizing = pickle.load(my_input)

            standard_gamma = gamma_standardizing.transform(gamma_data1)
            principalComponents_gamma = pca_gamma.transform(standard_gamma)
            gamma_data1 = pd.DataFrame(data=principalComponents_gamma)

            standard_beta = beta_standardizing.transform(beta_data1)
            principalComponents_beta = pca_beta.transform(standard_beta)
            beta_data1 = pd.DataFrame(data=principalComponents_beta)

            standard_alpha = alpha_standardizing.transform(alpha_data1)
            principalComponents_alpha = pca_alpha.transform(standard_alpha)
            alpha_data1 = pd.DataFrame(data=principalComponents_alpha)

            standard_theta = theta_standardizing.transform(theta_data1)
            principalComponents_theta = pca_theta.transform(standard_theta)
            theta_data1 = pd.DataFrame(data=principalComponents_theta)

            standard_delta = delta_standardizing.transform(delta_data1)
            principalComponents_delta = pca_delta.transform(standard_delta)
            delta_data1 = pd.DataFrame(data=principalComponents_delta)

            standard_merged = merged_standardizing.transform(merged)
            principalComponents_merged = pca_merged.transform(standard_merged)
            merged = pd.DataFrame(data=principalComponents_merged)

            predictions_gamma = dtree1.predict(gamma_data1)
            predictions_beta = dtree2.predict(beta_data1)
            predictions_alpha = dtree3.predict(alpha_data1)
            predictions_theta = dtree4.predict(theta_data1)
            predictions_delta = dtree5.predict(delta_data1)
            predictions_merged = dtree6.predict(merged)
            like = 0
            dislike = 0
            self.NextButton.show()
            self.NextButton.setText("Proceed")  # text
            self.NextButton.setStyleSheet("background-color: green;")
            self.NextButton.setShortcut('Ctrl+N')  # shortcut key
            self.NextButton.setGeometry(0, 0, 300, 100)
            self.NextButton.move(830, 700)
            self.label.setText("Please write Like/Dislike on the provided paper")
            self.label.setStyleSheet('color: white; text-align: center;margin-left:200px')
            if predictions_gamma != 'Dislike':
                like += 1
            else:
                dislike += 1
            if predictions_beta != 'Dislike':
                like += 1
            else:
                dislike += 1
            if predictions_alpha != 'Dislike':
                like += 1
            else:
                dislike += 1
            if predictions_theta != 'Dislike':
                like += 2
            else:
                dislike += 2
            if predictions_delta != 'Dislike':
                like += 1
            else:
                dislike += 1
            if predictions_merged != 'Dislike':
                like += 1
            else:
                dislike += 1
            print("like:", like, '\n', "Dislike:", dislike)
            if like >= dislike:
                self.NextButton.clicked.connect(lambda: self.predict("Liked"))
            else:
                self.NextButton.clicked.connect(lambda: self.predict("Dislike"))

            self.setStyleSheet("background-color: black;")
        except Exception as e:
            print(e)

    def finish(self):
        self.label.clear()
        self.NextButton.hide()
        self.NextButton2.hide()
        self.label.move(0, 0)
        self.setWindowTitle("done")
        self.setStyleSheet("background-color: black;")
        file = 'images/thank_you.jpg'
        image = QPixmap(file)
        image = image.scaled(1950, 1100)
        self.label.setPixmap(image)
        self.label.resize(image.width(), image.height())
        self.s.disconnect()

    def carf(self, row):
        for i, elect in row.items():
            elect -= statistics.mean(row)
            row[i] = elect
        return row

    def predict(self, text):
        try:
            self.label.clear()
            self.NextButton.hide()
            self.setWindowTitle("prediction")
            if text == "Dislike":
                self.setStyleSheet("background-color: red;")
                self.label.setStyleSheet('color: black; text-align: center;margin-left:200px')
            else:
                self.setStyleSheet("background-color: green;")
                self.label.setStyleSheet('color: white; text-align: center;margin-left:200px')
            self.label.setText("You " + text + " this photo")
            self.NextButton2.show()
            self.NextButton2.setText("Continue")  # text
            self.NextButton2.setStyleSheet("background-color: yellow;")
            self.NextButton2.setShortcut('Ctrl+N')  # shortcut key
            self.NextButton2.setGeometry(0, 0, 300, 100)
            self.NextButton2.move(830, 700)
            self.NextButton2.clicked.connect(lambda: self.black_screen())
        except Exception as e:
            print(e)


App = QApplication(sys.argv)
images = np.array([i + 1 for i in range(20)])
window = TestWindow(images)
window.beginEx()
sys.exit(App.exec())
