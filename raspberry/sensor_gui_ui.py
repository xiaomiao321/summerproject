# -*- coding: utf-8 -*-
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # 主布局：水平布局，左右各占一半
        self.main_layout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.main_layout.setObjectName("main_layout")
        self.main_layout.setSpacing(10)
        self.main_layout.setContentsMargins(10, 10, 10, 10)

        # 左侧：图表
        self.plot_widget = PlotCanvas(self.centralwidget, width=4, height=3)
        self.main_layout.addWidget(self.plot_widget)
        self.main_layout.setStretch(0, 1)  # 左侧占 50%

        # 右侧：标签和采样率控件
        self.right_layout = QtWidgets.QVBoxLayout()
        self.right_layout.setObjectName("right_layout")
        self.right_layout.setSpacing(15)
        self.right_layout.setContentsMargins(15, 15, 15, 15)

        # Labels for CO2, Temp, RH, Time
        self.co2_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)  # 增大字体
        self.co2_label.setFont(font)
        self.co2_label.setAlignment(QtCore.Qt.AlignCenter)
        self.co2_label.setObjectName("co2_label")
        self.right_layout.addWidget(self.co2_label)

        self.temp_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.temp_label.setFont(font)
        self.temp_label.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_label.setObjectName("temp_label")
        self.right_layout.addWidget(self.temp_label)

        self.rh_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(20)
        self.rh_label.setFont(font)
        self.rh_label.setAlignment(QtCore.Qt.AlignCenter)
        self.rh_label.setObjectName("rh_label")
        self.right_layout.addWidget(self.rh_label)

        self.time_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(18)  # 增大字体
        self.time_label.setFont(font)
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setObjectName("time_label")
        self.right_layout.addWidget(self.time_label)

        # Sampling rate input and button
        self.rate_layout = QtWidgets.QHBoxLayout()
        self.rate_label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)  # 增大字体
        self.rate_label.setFont(font)
        self.rate_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.rate_label.setObjectName("rate_label")
        
        self.rate_spinbox = QtWidgets.QSpinBox(self.centralwidget)
        self.rate_spinbox.setMinimum(1)
        self.rate_spinbox.setMaximum(60)
        self.rate_spinbox.setValue(5)
        self.rate_spinbox.setSuffix(" sec")
        font = QtGui.QFont()
        font.setPointSize(16)
        self.rate_spinbox.setFont(font)
        self.rate_spinbox.setObjectName("rate_spinbox")
        
        self.set_rate_button = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.set_rate_button.setFont(font)
        self.set_rate_button.setObjectName("set_rate_button")
        self.rate_layout.addWidget(self.rate_label)
        self.rate_layout.addWidget(self.rate_spinbox)
        self.rate_layout.addWidget(self.set_rate_button)
        self.right_layout.addLayout(self.rate_layout)

        # 右侧布局添加到主布局
        self.right_widget = QtWidgets.QWidget(self.centralwidget)
        self.right_widget.setLayout(self.right_layout)
        self.main_layout.addWidget(self.right_widget)
        self.main_layout.setStretch(1, 1)  # 右侧占 50%

        # 状态栏
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        font = QtGui.QFont()
        font.setPointSize(14)
        self.statusbar.setFont(font)
        MainWindow.setStatusBar(self.statusbar)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Sensor Data Monitor"))
        self.co2_label.setText(_translate("MainWindow", "CO2: N/A ppm"))
        self.temp_label.setText(_translate("MainWindow", "Temp: N/A °C"))
        self.rh_label.setText(_translate("MainWindow", "RH: N/A %"))
        self.time_label.setText(_translate("MainWindow", "Time: N/A"))
        self.rate_label.setText(_translate("MainWindow", "Sampling Rate:"))
        self.set_rate_button.setText(_translate("MainWindow", "Set Rate"))

class PlotCanvas(FigureCanvas):
    def __init__(self, parent=None, width=4, height=3, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        super().__init__(self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        
        self.xdata = []
        self.ydata_co2 = []
        self.ydata_temp = []
        self.ydata_rh = []
        
        self.init_plot()

    def init_plot(self):
        self.ax = self.fig.add_subplot(111)
        self.ax.set_title('Sensor Data Over Time', fontsize=16)  # 增大标题字体
        self.ax.set_xlabel('Time (seconds)', fontsize=14)  # 增大轴标签字体
        self.ax.set_ylabel('CO2 (ppm)', fontsize=14, color='red')
        self.line_co2, = self.ax.plot([], [], label='CO2 (ppm)', color='red', linewidth=2)

        self.ax2 = self.ax.twinx()
        self.ax2.set_ylabel('Temperature (°C)', fontsize=14, color='blue')
        self.line_temp, = self.ax2.plot([], [], label='Temperature (°C)', color='blue', linewidth=2)

        self.ax3 = self.ax.twinx()
        self.ax3.spines['right'].set_position(('outward', 60))
        self.ax3.set_ylabel('Humidity (%)', fontsize=14, color='green')
        self.line_rh, = self.ax3.plot([], [], label='Humidity (%)', color='green', linewidth=2)

        lines = [self.line_co2, self.line_temp, self.line_rh]
        labels = ['CO2 (ppm)', 'Temperature (°C)', 'Humidity (%)']
        self.ax.legend(lines, labels, loc='upper left', fontsize=12)  # 增大图例字体

        self.ax.grid(True, alpha=0.3)
        self.fig.tight_layout()
        self.draw()

    def update_plot(self, x, co2, temp, rh):
        self.xdata.append(x)
        self.ydata_co2.append(co2)
        self.ydata_temp.append(temp)
        self.ydata_rh.append(rh)

        max_points = 100
        if len(self.xdata) > max_points:
            self.xdata = self.xdata[-max_points:]
            self.ydata_co2 = self.ydata_co2[-max_points:]
            self.ydata_temp = self.ydata_temp[-max_points:]
            self.ydata_rh = self.ydata_rh[-max_points:]

        self.line_co2.set_data(self.xdata, self.ydata_co2)
        self.line_temp.set_data(self.xdata, self.ydata_temp)
        self.line_rh.set_data(self.xdata, self.ydata_rh)

        if self.xdata:
            self.ax.set_xlim(min(self.xdata), max(self.xdata))
            
            if self.ydata_co2:
                y_min = min(self.ydata_co2)
                y_max = max(self.ydata_co2)
                y_range = y_max - y_min
                margin = y_range * 0.1 if y_range > 0 else 10
                self.ax.set_ylim(y_min - margin, y_max + margin)

            if self.ydata_temp:
                y_min = min(self.ydata_temp)
                y_max = max(self.ydata_temp)
                y_range = y_max - y_min
                margin = y_range * 0.1 if y_range > 0 else 1
                self.ax2.set_ylim(y_min - margin, y_max + margin)

            if self.ydata_rh:
                y_min = min(self.ydata_rh)
                y_max = max(self.ydata_rh)
                y_range = y_max - y_min
                margin = y_range * 0.1 if y_range > 0 else 5
                self.ax3.set_ylim(y_min - margin, y_max + margin)

        self.draw()