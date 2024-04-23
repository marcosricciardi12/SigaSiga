import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel
from PyQt6.QtCore import QTimer
import cv2
import numpy as np
from datetime import datetime

class ImageGenerator(QMainWindow):
    def __init__(self):
        super().__init__()

        self.title = 'Generador de Imágenes'
        self.left = 100
        self.top = 100
        self.width = 640
        self.height = 480

        self.initUI()
        self.initImage()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.label1 = QLabel('Nombre Equipo Local:', self)
        self.label1.move(20, 20)
        self.team_local = QLineEdit(self)
        self.team_local.move(180, 20)

        self.label2 = QLabel('Nombre Equipo Visitante:', self)
        self.label2.move(20, 50)
        self.team_visitor = QLineEdit(self)
        self.team_visitor.move(180, 50)

        self.label3 = QLabel('Puntos Equipo Local:', self)
        self.label3.move(20, 80)
        self.points_local = QLabel('0', self)
        self.points_local.move(180, 80)
        self.button1 = QPushButton('+', self)
        self.button1.move(230, 80)
        self.button1.clicked.connect(self.addPointLocal)
        self.button2 = QPushButton('-', self)
        self.button2.move(260, 80)
        self.button2.clicked.connect(self.removePointLocal)

        self.label4 = QLabel('Puntos Equipo Visitante:', self)
        self.label4.move(20, 110)
        self.points_visitor = QLabel('0', self)
        self.points_visitor.move(180, 110)
        self.button3 = QPushButton('+', self)
        self.button3.move(230, 110)
        self.button3.clicked.connect(self.addPointVisitor)
        self.button4 = QPushButton('-', self)
        self.button4.move(260, 110)
        self.button4.clicked.connect(self.removePointVisitor)

        self.label5 = QLabel('Tiempo:', self)
        self.label5.move(20, 140)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateTime)
        self.time_label = QLabel('', self)
        self.time_label.move(180, 140)
        self.timer.start(1000)

        self.start_button = QPushButton('Iniciar', self)
        self.start_button.move(20, 170)
        self.start_button.clicked.connect(self.startImageGeneration)

    def initImage(self):
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        self.current_time = ''
        self.image_counter = 0

    def generateImage(self):
        frame = np.zeros((480, 640, 3), np.uint8)
        cv2.putText(frame, 'Nombre Equipo Local: ' + self.team_local.text(), (10, 50), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Nombre Equipo Visitante: ' + self.team_visitor.text(), (10, 100), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Puntos Equipo Local: ' + self.points_local.text(), (10, 150), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Puntos Equipo Visitante: ' + self.points_visitor.text(), (10, 200), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        cv2.putText(frame, 'Tiempo: ' + self.current_time, (10, 250), self.font, 1, (255, 255, 255), 2, cv2.LINE_AA)

        filename = 'flask/test_frame.jpg'
        cv2.imwrite(filename, frame)
        self.image_counter += 1

    def startImageGeneration(self):
        self.generateImage()
        self.timer_image = QTimer(self)
        self.timer_image.timeout.connect(self.generateImage)
        self.timer_image.start(2) # 0.33 seconds

    def addPointLocal(self):
        points = int(self.points_local.text())
        points += 1
        self.points_local.setText(str(points))

    def removePointLocal(self):
        points = int(self.points_local.text())
        points -= 1
        self.points_local.setText(str(points))

    def addPointVisitor(self):
        points = int(self.points_visitor.text())
        points += 1
        self.points_visitor.setText(str(points))

    def removePointVisitor(self):
        points = int(self.points_visitor.text())
        points -= 1
        self.points_visitor.setText(str(points))

    def updateTime(self):
        now = datetime.now()
        self.current_time = now.strftime("%H:%M:%S")
        self.time_label.setText(self.current_time)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageGenerator()
    ex.show()
    sys.exit(app.exec())