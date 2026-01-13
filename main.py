import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QLCDNumber, QLabel, QVBoxLayout, QWidget
from psuedoSensor import PseudoSensor

# app = QApplication(sys.argv)

# # window = QPushButton("Push Me")
# window = QMainWindow()
# window.show()

# app.exec()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Application Success")
        self.setFixedSize(QSize(200,400))

        self.ps = PseudoSensor()

        button = QPushButton("Read Sensor")
        button.clicked.connect(self.button_clicked)

        self.humidity_label = QLabel("Humidity: --")
        self.temp_label = QLabel("Temperatur: --")

        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.temp_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)   

        # self.setCentralWidget(button)
    
    def button_clicked(self):
        h,t = self.ps.generate_values()
        self.humidity_label.setText(f"Humidity: {h}")
        self.temp_label.setText(f"Temperature: {t}")
        print(f"Humidity: {h}, Temp {t}")
    
app = QApplication(sys.argv)


window = MainWindow()
window.show()
app.exec()
    


ps = PseudoSensor()

# for i in range(30):

#     h,t = ps.generate_values()

#     print("i ",i)

#     print("H ",h)

#     print("T ",t)


