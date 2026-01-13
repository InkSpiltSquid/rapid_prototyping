from PyQt6.QtWidgets import QApplication, QWidget
import sys
import psuedoSensor

ps = psuedoSensor.PseudoSensor()

app = QApplication(sys.argv)
window = QWidget()
window.show()

app.exec
# for i in range(30):

#     h,t = ps.generate_values()

#     print("i ",i)

#     print("H ",h)

#     print("T ",t)