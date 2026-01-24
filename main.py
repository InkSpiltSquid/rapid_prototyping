import sys
from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QMainWindow, QLCDNumber, QLabel, QVBoxLayout, QWidget, QLineEdit, QHBoxLayout, QScrollArea
from psuedoSensor import PseudoSensor
from dataBase import SensorDatabase
import datetime
import time


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.toggle_units = 0
        self.units = "F"
        self.setWindowTitle("Sensor Reader with DataBase")
        self.setFixedSize(QSize(500,700))

        self.ps = PseudoSensor()
        self.db = SensorDatabase()

        button = QPushButton("Read Sensor")
        button.clicked.connect(self.button_clicked)

        unit_button = QPushButton("Change Units")
        unit_button.setCheckable(True)
        unit_button.clicked.connect(self.unit_button_clicked)

        view_data_button = QPushButton("View Stored Data")
        view_data_button.clicked.connect(self.view_data_clicked)

        temp_threshold_layout = QHBoxLayout()
        temp_threshold_layout.addWidget(QLabel("Temp Alarm (°F):"))
        self.temp_threshold_input = QLineEdit("194")
        temp_threshold_layout.addWidget(self.temp_threshold_input)

        humidity_threshold_layout = QHBoxLayout()
        humidity_threshold_layout.addWidget(QLabel("Humidity Alarm (%):"))
        self.humidity_threshold_input = QLineEdit("80")
        humidity_threshold_layout.addWidget(self.humidity_threshold_input)


        self.display_area = QLabel("Welcome! Click 'Read Sensor' to begin")
        self.display_area.setWordWrap(True)
        self.display_area.setAlignment(Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft)
        self.display_area.setStyleSheet("padding: 10px; border: 1px solid gray;")

        ten_to_collect = QPushButton("Collect 10")
        ten_to_collect.clicked.connect(self.ten_collects)

        kill_program = QPushButton("Kill GUI")
        kill_program.clicked.connect(QApplication.quit)


        layout = QVBoxLayout()
        layout.addWidget(button)
        layout.addWidget(unit_button)
        layout.addWidget(ten_to_collect)
        layout.addWidget(view_data_button)
        layout.addLayout(temp_threshold_layout)
        layout.addLayout(humidity_threshold_layout)
        layout.addWidget(self.display_area)
        layout.addWidget(kill_program)

        container = QWidget()
        container.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(container)
        scroll.setWidgetResizable(True)
        self.setCentralWidget(scroll)   

    
    def button_clicked(self):
        """ Single Read sensor button """
        h,t = self.ps.generate_values()     # calling from PsuedoSensor.py
        self.db.add_reading(t, h)   # adding read to the database
        alert_status = self.check_alerts(h, t)  # Determine temperature display and alert status
        if self.toggle_units == 0:  # Checking what toggle_units is set to for temperature Units (Fahrenheit <=> Celsius)
            t_display = (t * 9/5) + 32
            temp_text = f"{t_display:.3f} °F"
            unit = "Fahrenheit"
        else:
            temp_text = f"{t:.3f} °C"
            unit = "Celsius"

       
        display_text = f"""**========** CURRENT READING **========**

Humidity: {h:.3f}%
Temperature: {temp_text}

{alert_status}
"""
        self.display_area.setText(display_text)     # Display within the GUI terminal
        return h, t
    
    def unit_button_clicked(self):
        """ Sets toggle_units for conversion """
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
        """Check thresholds from user input fields and return alert status"""
        try:
            TEMP_THRESHOLD = float(self.temp_threshold_input.text())    # Read threshold values from input fields
            HUMIDITY_THRESHOLD = float(self.humidity_threshold_input.text())
        except ValueError:
            return "Invalid alarm threshold values!"

        alerts = []

        
        if self.toggle_units == 1:      # Convert temperature to Fahrenheit for comparison if needed
            temp_check = (temperature * 9/5) + 32
        else:
            temp_check = temperature    # Already in Fahrenheit
        if temp_check > TEMP_THRESHOLD:     # Check temperature against threshold
            alerts.append("ALERT: Temperature EXCEEDS alarm threshold!")
        if humidity > HUMIDITY_THRESHOLD:    # Check humidity against threshold
            alerts.append("ALERT: Humidity EXCEEDS alarm threshold!")
        if alerts:
            return "\n".join(alerts)
        else:
            return "All readings normal"


    def view_data_clicked(self):
        """ Pull previous reads from dataBase.py """
        readings = self.db.get_recent_readings(10)
        if not readings:
            self.display_area.setText("No readings stored yet!")
            return

        temps = [reading[2] for reading in readings]
        humidities = [reading[3] for reading in readings]
        """ finds min, max, and the average of temps and humidity """
        temp_min = min(temps)
        temp_max = max(temps)
        temp_avg = sum(temps) / len(temps)

        humidity_min = min(humidities)
        humidity_max = max(humidities)
        humidity_avg = sum(humidities) / len(humidities)

        data_text = f"""**========** LAST 10 READINGS STATISTICS **========**

Temperature (C):
   Minimum: {temp_min:.3f}
   Maximum: {temp_max:.3f}
   Average: {temp_avg:.3f}

Humidity (%):
   Minimum: {humidity_min:.3f}
   Maximum: {humidity_max:.3f}
   Average: {humidity_avg:.3f}

**========** DETAILED READINGS **========**

"""
        for reading in readings:
            data_text += f"ID: {reading[0]} | {reading[1]}\n"
            data_text += f"   Temp: {reading[2]:.3f}°C | Humidity: {reading[3]:.3f}%\n\n"

        self.display_area.setText(data_text)

    def ten_collects(self):
        """ Collects 10 psuedoSensor readings with a 1 second pause in between """
        all_data = "═══ COLLECTING 10 READINGS ═══\n\n"
        for i in range(10):
            h, t = self.button_clicked()
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            all_data += f"Reading {i+1}/10 | {timestamp}\n"
            all_data += f"   Temp: {t:.3f} {self.units} | Humidity: {h:.3f}%\n\n"
            time.sleep(1)
        self.display_area.setText(all_data)



    def closeEvent(self, event):
        self.db.close()
        event.accept()

    
app = QApplication(sys.argv)


window = MainWindow()
window.show()
app.exec()



