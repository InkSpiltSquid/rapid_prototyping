import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QLCDNumber, QLabel, QVBoxLayout, QWidget
from psuedoSensor import PseudoSensor
from dataBase import SensorDatabase
import datetime
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
        self.collect = QLabel("10 Data Points")

        self.last10 = QLabel("=== Last 10 Readings ===")
        self.recorded_data = QLabel("Click 'View Stored Data' to see readings")

        ten_to_collect = QPushButton("10 to Collect")
        ten_to_collect.clicked.connect(self.ten_collects)

        kill_program = QPushButton("Kill GUI")
        kill_program.clicked.connect(QApplication.quit)


        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(self.humidity_label)
        layout.addWidget(self.temp_label)
        layout.addWidget(unit_button)
        layout.addWidget(view_data_button)
        layout.addWidget(self.last10)
        layout.addWidget(self.recorded_data)
        layout.addWidget(ten_to_collect)
        layout.addWidget(self.collect)
        layout.addWidget(kill_program)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)   

        # self.setCentralWidget(button)
    
    def button_clicked(self):
        h,t = self.ps.generate_values()

        self.db.add_reading(t, h)

        self.check_alerts(h, t)

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

    def check_alerts(self, humidity, temperature):

        if self.toggle_units == 1:
            TEMP_HIGH = 90  # Celsius
            TEMP_LOW = 0   # Celsius
        else:
            TEMP_HIGH = 194 # Far
            TEMP_LOW = -32  # Far

        HUMIDITY_HIGH = 80  
        HUMIDITY_LOW = 15   


        self.temp_label.setStyleSheet("")
        self.humidity_label.setStyleSheet("")

        if temperature > TEMP_HIGH:
            self.temp_label.setStyleSheet("color: red; font-weight: bold;")
        elif temperature < TEMP_LOW:
            self.temp_label.setStyleSheet("color: blue; font-weight: bold;")

        if humidity > HUMIDITY_HIGH:
            self.humidity_label.setStyleSheet("color: red; font-weight: bold;")
        elif humidity < HUMIDITY_LOW:
            self.humidity_label.setStyleSheet("color: orange; font-weight: bold;")


    def view_data_clicked(self):
        readings = self.db.get_recent_readings(10)
        if not readings:
            self.recorded_data.setText("No readings stored yet!")
            return
        data_text = ""
        for reading in readings:
            data_text += f"ID: {reading[0]} | Time: {reading[1]} | Temp: {reading[2]:.3f} {self.units} | Humidity: {reading[3]:.3f}%\n"

        self.recorded_data.setText(data_text)

    def ten_collects(self):
        all_data = ""
        for i in range(10):
            h, t = self.button_clicked()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_data += f"ID: {i} | Time: {timestamp} | Temp: {t:.3f} {self.units} | Humidity: {h:.3f}%\n"
            time.sleep(1)
        self.collect.setText(all_data)



    def closeEvent(self, event):
        self.db.close()
        event.accept()

    
app = QApplication(sys.argv)


window = MainWindow()
window.show()
app.exec()



