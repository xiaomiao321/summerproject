# -*- coding: utf-8 -*-
import sys
import os
import time
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from sensor_gui_ui import Ui_MainWindow

class SensorGUI(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.log_file = "/home/xiaomiao/sensor_data.log"
        self.rate_file = "/home/xiaomiao/sampling_rate.conf"
        
        self.start_time = time.time()

        self.set_rate_button.clicked.connect(self.set_rate)

        if os.path.exists(self.rate_file):
            with open(self.rate_file, 'r') as f:
                try:
                    rate_value = int(f.read().strip())
                    self.rate_spinbox.setValue(rate_value)
                except ValueError:
                    self.statusbar.showMessage("Invalid sampling rate in config file, using default 5s", 5000)
                    self.rate_spinbox.setValue(5)
        else:
            self.rate_spinbox.setValue(5)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_data)
        self.start_timer()

    def start_timer(self):
        rate_value = self.rate_spinbox.value()
        self.timer.stop()
        self.timer.start(rate_value * 1000)

    def set_rate(self):
        new_rate = self.rate_spinbox.value()
        if new_rate > 0:
            try:
                with open(self.rate_file, 'w') as f:
                    f.write(str(new_rate))
                self.start_timer()
                self.statusbar.showMessage(f"Sampling rate set to {new_rate} seconds", 5000)
                print(f"Sampling rate set to {new_rate} seconds")
            except Exception as e:
                self.statusbar.showMessage(f"Failed to save sampling rate: {e}", 5000)
                print(f"Error saving sampling rate: {e}")

    def update_data(self):
        try:
            if os.path.exists(self.log_file):
                with open(self.log_file, 'r') as f:
                    lines = f.readlines()
                    if lines:
                        last_line = lines[-1].strip()
                        try:
                            timestamp, data = last_line.split(': ', 1)
                            co2 = float(data.split(', ')[0].split('=')[1])
                            temp = float(data.split(', ')[1].split('=')[1])
                            rh = float(data.split(', ')[2].split('=')[1])

                            elapsed_time = time.time() - self.start_time
                            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            self.co2_label.setText(f"CO2: {co2:.1f} ppm")
                            self.temp_label.setText(f"Temp: {temp:.1f} °C")
                            self.rh_label.setText(f"RH: {rh:.1f} %")
                            self.time_label.setText(f"Time: {current_time}")

                            self.plot_widget.update_plot(elapsed_time, co2, temp, rh)
                            
                        except (ValueError, IndexError) as e:
                            print(f"Error parsing log line: {last_line}")
                            print(f"Parse error: {e}")
                            self.co2_label.setText("CO2: Parse Error")
                            self.temp_label.setText("Temp: Parse Error")
                            self.rh_label.setText("RH: Parse Error")
                            self.time_label.setText(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                            
            else:
                current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.co2_label.setText("CO2: Waiting for data...")
                self.temp_label.setText("Temp: Waiting for data...")
                self.rh_label.setText("RH: Waiting for data...")
                self.time_label.setText(f"Time: {current_time}")
                
        except Exception as e:
            print(f"Error reading log file: {e}")
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.co2_label.setText("CO2: Read Error")
            self.temp_label.setText("Temp: Read Error")
            self.rh_label.setText("RH: Read Error")
            self.time_label.setText(f"Time: {current_time}")

    def closeEvent(self, event):
        self.timer.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SensorGUI()
    window.show()
    sys.exit(app.exec_())