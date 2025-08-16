import sys
import json
from dataclasses import dataclass

from PyQt5.QtWidgets import (QApplication, QComboBox, QMainWindow, QWidget,
                             QVBoxLayout, QHBoxLayout, QLabel, QMessageBox, QPushButton, QCheckBox, QDialog)
from lunar_python import Lunar, LunarMonth, SolarYear, Solar
from lunar_python import LunarYear
from lunar_python.util import SolarUtil, LunarUtil

# 1. 定义结构体
from BaziDialog import BaziDialog, BaZiDetail



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.button_OK = None
        self.check_zaowanzishi = None
        self.check_truesolar = None
        self.month_space = None
        self.month_combo = None
        self.month_label = None
        self.year_space = None
        self.year_combo = None
        self.year_label = None
        self.solar_space = None
        self.lunarOrSolar_combo = None
        self.lunarOrSolar_label = None
        self.btn_taiyangshi = None
        self.district_combo = None
        self.district_label = None
        self.day_label = None
        self.city_combo = None
        self.city_label = None
        self.province_combo = None
        self.province_label = None
        self.day_combo = None
        self.wd = None
        self.jd = None
        self.data = None  # 存储行政区划数据
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.setWindowTitle("中国行政区划选择器")
        self.setGeometry(100, 100, 400, 200)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 主布局
        main_layout = QVBoxLayout(central_widget)

        # -------------第一行显示-------------------------
        # 行政区划选择布局
        selection_layout = QHBoxLayout()

        # 省份选择
        self.province_label = QLabel("省份/直辖市/自治区：")
        self.province_combo = QComboBox()
        self.province_combo.currentTextChanged.connect(self.on_province_changed)

        # 城市选择
        self.city_label = QLabel("城市：")
        self.city_combo = QComboBox()
        self.city_combo.currentTextChanged.connect(self.on_city_changed)

        # 区县选择
        self.district_label = QLabel("区/县：")
        self.district_combo = QComboBox()
        # self.district_label.currentTextChanged.connect(self.on_district_changed)
        self.district_combo.currentTextChanged.connect(self.on_jwd_changed)

        # 进行经纬度查询以及太阳时的计算并输出
        # self.btn_taiyangshi = QPushButton("太阳时");
        # self.btn_taiyangshi.clicked.connect(self.btn_taiyangshi_clicked)

        # 添加到布局
        selection_layout.addWidget(self.province_label)
        selection_layout.addWidget(self.province_combo)
        selection_layout.addWidget(self.city_label)
        selection_layout.addWidget(self.city_combo)
        selection_layout.addWidget(self.district_label)
        selection_layout.addWidget(self.district_combo)
        # selection_layout.addWidget(self.btn_taiyangshi)

        # -------------第2行显示-------------------------
        date_layout = QHBoxLayout()
        self.lunarOrSolar_label = QLabel("公历/农历")
        self.lunarOrSolar_combo = QComboBox();
        self.lunarOrSolar_combo.addItem("公历")
        self.lunarOrSolar_combo.addItem("农历")
        self.solar_space = QLabel("        ")

        self.year_label = QLabel("年")
        self.year_combo = QComboBox();
        for n in range(1900, 2025):
            self.year_combo.addItem(str(n))
        self.year_space = QLabel("        ")

        self.month_label = QLabel("月")
        self.month_combo = QComboBox();
        for n in range(1, 13):  # 显示12个月的
            self.month_combo.addItem(str(n) + "月")
        self.month_combo.setMinimumWidth(120)
        # self.month_combo.setSpacing(15)
        self.month_space = QLabel("        ")

        self.day_label = QLabel("日")
        self.day_combo = QComboBox();
        # self.day_combo.addItem("1日")
        for n in range(1, 31):
            self.day_combo.addItem(str(n))

        self.lunarOrSolar_combo.currentTextChanged.connect(self.on_solar_lunar_changed)
        self.month_combo.currentTextChanged.connect(self.on_month_changed)
        self.day_combo.currentTextChanged.connect(self.on_day_changed)
        self.year_combo.currentTextChanged.connect(self.on_year_changed)

        self.check_truesolar = QCheckBox("真太阳时")
        self.check_zaowanzishi = QCheckBox("早晚子时")
        self.button_OK = QPushButton("开始计算")

        # 添加到布局
        date_layout.addWidget(self.lunarOrSolar_label)
        date_layout.addWidget(self.lunarOrSolar_combo)
        date_layout.addWidget(self.solar_space)

        date_layout.addWidget(self.year_label)
        date_layout.addWidget(self.year_combo)
        date_layout.addWidget(self.year_space)

        date_layout.addWidget(self.month_label)
        date_layout.addWidget(self.month_combo)
        date_layout.addWidget(self.month_space)

        date_layout.addWidget(self.day_label)
        date_layout.addWidget(self.day_combo)

        date_layout.addWidget(self.check_truesolar)
        date_layout.addWidget(self.check_zaowanzishi)
        date_layout.addWidget(self.button_OK)
        self.button_OK.clicked.connect(self.btn_OK_clicked)

        # 总布局
        main_layout.addLayout(selection_layout)
        main_layout.addLayout(date_layout)

    def on_solar_lunar_changed(self):
        # 月日要变化,年份不变
        solarOrlunar = self.lunarOrSolar_combo.currentText()
        self.month_combo.clear()
        self.day_combo.clear()

        # // 阻止Combo2发送信号
        self.month_combo.blockSignals(True);
        self.day_combo.blockSignals(True);

        yearNow = self.year_combo.currentText()
        daysInMonth = 0
        if solarOrlunar == "农历":
            lunarYear = LunarYear.fromYear(int(yearNow))
            months = lunarYear.getMonthsInYear()
            # if months.count() > 12:#有闰月
            #     leapmonth = lunarYear.getLeapMonth()
            for month in months:
                # self.month_combo.addItem(month.toString())
                parts = month.toString().split('年')  # 分割为 ["1905", "五月(29天)"]
                # month_part = parts[1].split('(')[0]  # 提取 "五月"
                self.month_combo.addItem(parts[1])

            daysInMonth = LunarMonth.fromYm(int(yearNow), 1).getDayCount()
        else:
            for n in range(1, 13):  # 显示12个月的
                self.month_combo.addItem(str(n) + "月")
            daysInMonth = 31

        for n in range(1,daysInMonth+1):
            self.day_combo.addItem(str(n))

        # // 恢复信号发送
        self.month_combo.blockSignals(False)
        self.month_combo.blockSignals(False)

    def btn_OK_clicked(self):
        # 此时已经获取到经纬度信息了
        # 根据经纬度计算真太阳时
        print(f"btn_taiyangshi_clicked-----jd={self.jd},wd={self.wd}")

        solar = Solar(1987, 2, 2, 21, 30, 0)
        lunar = solar.getLunar()
        baZi = lunar.getEightChar()
        print(baZi.getYear() + ' ' + baZi.getMonth() + ' ' + baZi.getDay() + ' ' + baZi.getTime())

        # //传递给下一个页面并显示
        """打开模态对话框并传递参数"""
        # 准备要传递的参数
        baziDetail = BaZiDetail(
            name = "ABC",
            gender = "男",
            year_is_solar_not_lunar = True,
            year= "1987",
            month="2",
            day="2",
            hour="21",
            minute="30",
            province= "ssss",
            city= "ssss",
            distinct= "ssss",
            truesolar= False,
            zaowanzishi= False
        )

        # 创建模态对话框实例，传递参数和父窗口
        main_window = BaziDialog(baziDetail, self)

        # 关键步骤：关闭当前主窗口
        self.close()

        # 以模态方式显示（exec_()会阻塞当前窗口，直到对话框关闭）
        # result = dialog.exec_()
        # 对话框关闭后可获取返回结果（如果需要）
        # if result == QDialog.Accepted:
        #     print("对话框被确认关闭")
        # else:
        #     print("对话框被取消关闭")

        main_window.show()
        # sys.exit(app.exec_())





    def on_year_changed(self):
        solarOrlunar = self.lunarOrSolar_combo.currentText()
        self.month_combo.clear()

        yearNow = self.year_combo.currentText()
        if solarOrlunar == "农历":
            lunarYear = LunarYear.fromYear(int(yearNow))
            months = lunarYear.getMonthsInYear()
            # if months.count() > 12:#有闰月
            #     leapmonth = lunarYear.getLeapMonth()
            for month in months:
                # self.month_combo.addItem(month.toString())
                parts = month.toString().split('年')  # 分割为 ["1905", "五月(29天)"]
                # month_part = parts[1].split('(')[0]  # 提取 "五月"
                self.month_combo.addItem(parts[1])
        else:
            for n in range(1, 13):  # 显示12个月的
                self.month_combo.addItem(str(n) + "月")

    def on_month_changed(self):
        solarOrlunar = self.lunarOrSolar_combo.currentText()
        self.day_combo.clear()

        # // 阻止Combo2发送信号
        self.day_combo.blockSignals(True)

        yearNow = self.year_combo.currentText()
        monthIndex = self.month_combo.currentIndex()
        monthName = self.month_combo.currentText()
        if monthIndex < 0:
            return

        if solarOrlunar == "农历":
            lunarYear = LunarYear.fromYear(int(yearNow))
            if lunarYear.getLeapMonth() == 0:  # 没有闰月
                daysInMonth = LunarMonth.fromYm(int(yearNow), monthIndex + 1).getDayCount()
                for n in range(1, daysInMonth + 1):
                    self.day_combo.addItem(str(n))
            else:
                lunarMonth = self.lunar_month_to_num(monthName)
                if -1 != monthName.find('闰'):
                    # days = LunarUtil.getDaysOfMonth(int(yearNow, -lunarMonth))
                    days = LunarMonth.fromYm(int(yearNow), -lunarMonth).getDayCount()
                else:
                    # days = LunarUtil.getDaysOfMonth(int(yearNow, lunarMonth))
                    days = LunarMonth.fromYm(int(yearNow), lunarMonth).getDayCount()

            for n in range(1, days + 1):
                self.day_combo.addItem(str(n))
        else:
            # 是否闰月？闰月2月29天
            if SolarUtil.isLeapYear(int(yearNow)):
                if monthIndex == 1:
                    for n in range(1, 30):
                        self.day_combo.addItem(str(n))
        for n in range(1, SolarUtil.getDaysOfMonth(int(yearNow), monthIndex + 1)+1):
            self.day_combo.addItem(str(n))
        # pass

        # // 恢复信号发送
        self.day_combo.blockSignals(False)

    def on_day_changed(self):
        pass

    def lunar_month_to_num(self, month_str):
        """将农历月份（如正月、腊月）转换为数字"""
        lunar_map = {
            '正月': 1, '二月': 2, '三月': 3, '四月': 4, '五月': 5,
            '六月': 6, '七月': 7, '八月': 8, '九月': 9, '十月': 10,
            '冬月': 11, '腊月': 12
        }
        # 处理"闰月"情况
        if month_str.startswith('闰'):
            base_month = month_str[1:]  # 去除"闰"字
            return lunar_map.get(base_month, None)

        # return lunar_map.get(month_str, None)
        # 优先用分割法，简洁高效
        return lunar_map.get(month_str.split('(')[0], None)

    def num_to_month(self, month_num):
        """将农历月份（如正月、腊月）转换为数字"""
        lunar_map = {
            '正月': 1, '二月': 2, '三月': 3, '四月': 4, '五月': 5,
            '六月': 6, '七月': 7, '八月': 8, '九月': 9, '十月': 10,
            '冬月': 11, '腊月': 12
        }
        # # 处理"闰月"情况
        # if month_str.startswith('闰'):
        #     base_month = month_str[1:]  # 去除"闰"字
        #     return lunar_map.get(base_month, None)

        return lunar_map.get(None, month_num)

    def on_jwd_changed(self, district_name):
        print("on_jwd_changed,district_name=" + district_name)

        # 获取当前选中的省份
        if not self.city_combo or self.city_combo.currentIndex() < 0:
            print("self.city_combo is null")
            return

        print("on_jwd_changed,000" + self.city_combo.currentText())
        city = self.city_combo.currentData()
        # print("on_jwd_changed,city=" + city)

        # 安全检查
        if not city:
            print("未选择城市")
            return

        # # 找到选中的城市数据
        for distirct in city.get('counties', []):
            if distirct['name'] == district_name:
                self.jd = distirct.get("center")[0]
                self.wd = distirct.get("center")[1]
                print(f"jd={self.jd},wd={self.wd}")
                # print("jwd="+distirct['center'])
                break

    def load_data(self):
        """加载行政区划数据"""
        try:
            with open('china_administrative_divisions.json', 'r', encoding='utf-8') as f:
                self.data = json.load(f)

            # 初始化省份下拉框
            self.province_combo.clear()
            for province in self.data.get('provinces', []):
                self.province_combo.addItem(province['name'], province)

        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "未找到行政区划数据文件！")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "错误", "行政区划数据文件格式错误！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据时发生未知错误：{str(e)}")

    def on_province_changed(self, province_name):
        """省份选择变化时更新城市下拉框"""
        if not self.data:
            return

        # 找到选中的省份数据
        for province in self.data.get('provinces', []):
            if province['name'] == province_name:
                # 清空城市和区县下拉框
                self.city_combo.clear()
                self.district_combo.clear()

                # 更新城市下拉框
                for city in province.get('cities', []):
                    self.city_combo.addItem(city['name'], city)
                break

    def on_city_changed(self, city_name):
        """城市选择变化时更新区县下拉框"""
        if not self.data or self.province_combo.currentIndex() < 0:
            return

        # 获取当前选中的省份
        province = self.province_combo.currentData()

        # 找到选中的城市数据
        for city in province.get('cities', []):
            if city['name'] == city_name:
                # 清空区县下拉框
                self.district_combo.clear()

                # 更新区县下拉框
                for district in city.get('counties', []):
                    self.district_combo.addItem(district['name'])
                break


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
