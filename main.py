import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QLCDNumber, QLabel, QVBoxLayout, QWidget
from psuedoSensor import PseudoSensor
from dataBase import SensorDatabase
import time


# app = QApplication(sys.argv)

# # window = QPushButton("Push Me")
# window = QMainWindow()
# window.show()

# app.exec()

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.toggle_units = 0
        self.units = "F"
        self.setWindowTitle("Sensor Reader with DataBase")
        # self.setFixedSize(QSize(200,400))

        self.ps = PseudoSensor()
        self.db = SensorDatabase()

        button = QPushButton("Read Sensor")
        button.clicked.connect(self.button_clicked)

        unit_button = QPushButton("Change Units")
        unit_button.setCheckable(True)
        unit_button.clicked.connect(self.unit_button_clicked)

        view_data_button = QPushButton("View Stored Data")
        view_data_button.clicked.connect(self.view_data_clicked)

        self.humidity_label = QLabel("Humidity: -- %")
        self.temp_label = QLabel("Temperature: --")

        self.last10 = QLabel("=== Last 10 Readings ===")
        self.recorded_data = QLabel("Click 'View Stored Data' to see readings")

        10_to_collect = QPushButton("10 to Collect")
        10_to_collect.clicked.connect(self.ten_collects)


        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(unit_button)
        layout.addWidget(view_data_button)
        layout.addWidget(self.last10)
        layout.addWidget(self.recorded_data)
        layout.addWidget(10_to_collect)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)   

        # self.setCentralWidget(button)
    
    def button_clicked(self):
        h,t = self.ps.generate_values()

        # Save to database (always save raw Celsius values)
        self.db.add_reading(t, h)

        self.humidity_label.setText(f"Humidity: {h:.3f} %")
        if self.toggle_units == 0:
            t_display = (t * 9/5) + 32
            self.temp_label.setText(f"Temperature: {t_display:.3f} Fahrenheit")
        else:
            self.temp_label.setText(f"Temperature: {t:.3f} Celsius")
        return h, t
    
    def unit_button_clicked(self):
        if self.sender().isChecked():
            self.toggle_units = 1
            print("Button is ON - switching to Fahrenheit")
            self.units = "C"
        else:
            self.toggle_units = 0
            print("button is OFF - switching to Celsius")
            self.units = "F"
        return self.units

    
    def view_data_clicked(self):
        readings = self.db.get_recent_readings(10)
        if not readings:
            self.recorded_data.setText("No readings stored yet!")
            return
        # Build a string with all readings
        data_text = ""
        for reading in readings:
            data_text += f"ID: {reading[0]} | Time: {reading[1]} | Temp: {reading[2]:.3f} {self.units} | Humidity: {reading[3]:.3f}%\n"

        self.recorded_data.setText(data_text)

    def ten_collects(self):
        for _ in range(10):
            h, t = button_clicked()
            self.record.setText(f"ID: {_} | Time: {time} | Temp {t} {self.units} | Humidity: {h}")
            time.sleep(1)

    def closeEvent(self, event):
        self.db.close()
        event.accept()

    
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


