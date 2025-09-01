import json
import sys
from datetime import datetime

from PyQt5.QtWidgets import QWidget, QMessageBox, QApplication, QMainWindow
from PyQt5.uic import loadUi
from lunar_python import LunarYear, LunarMonth, Solar
from lunar_python.util import SolarUtil

from BaziDialog import BaziDialog, BaZiDetail
from static_ganzhi_yinyang import GanZhiYinYang
from time_offset_calculator import calculate_time_offset, datetime_add_minutes


class UserInfoWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.tiangan = None
        self.wd = None
        self.gender = None
        self.jd = None
        self.data = None
        self.comboBox_chushengnianfeng = None
        self.comboBox_year = None
        self.comboBox_ri = None
        self.comboBox_yangliyingli = None
        self.comboBox_yue = None
        self.year_label = None
        self.init_ui()

    def init_ui(self):
        # 加载UI文件
        # loadUi("BaziDialog.ui", self)
        loadUi("userinfo.ui", self)

        # //初始化数据------出生地-出生时间
        # for n in range(1900, 2025):
        #     self.comboBox_year.addItem(str(n))
        self.comboBox_year.clear()
        for n in range(2025,1949,-1):
            self.comboBox_year.addItem(str(n))

        self.comboBox_yue.clear()
        for n in range(1, 13):  # 显示12个月的
            self.comboBox_yue.addItem(str(n))

        self.comboBox_ri.clear()
        for n in range(1, 31):
            self.comboBox_ri.addItem(str(n))

        # //初始化数据------八字干支
        for n in range(1900, 2025):
            self.comboBox_chushengnianfeng.addItem(str(n))

        self.comboBox_yangliyingli.currentTextChanged.connect(self.on_solar_lunar_changed)
        self.comboBox_yue.currentTextChanged.connect(self.on_month_changed)
        self.comboBox_ri.currentTextChanged.connect(self.on_day_changed)
        self.comboBox_year.currentTextChanged.connect(self.on_year_changed)

        self.comboBox_borntime.currentTextChanged.connect(self.on_inputinfo_changed)
        self.pushButton_OK.clicked.connect(self.btn_OK_clicked)

        # 省份选择
        self.comboBox_sheng.currentTextChanged.connect(self.on_province_changed)

        # 城市选择
        self.comboBox_shi.currentTextChanged.connect(self.on_city_changed)

        # # 区县选择
        # self.comboBox_xian.currentTextChanged.connect(self.on_xian_changed)

        # 性别选择
        self.comboBox_gender.currentTextChanged.connect(self.on_gender_changed)

        # 时分秒的选择
        for n in range(24):
            self.comboBox_hour.addItem(str(n))

        for n in range(60):
            self.comboBox_feng.addItem(str(n))

        for n in range(60):
            self.comboBox_miao.addItem(str(n))

        # 天干地支的选择
        self.tiangan = ["甲", "乙", "丙", "丁", "戊", "己", "庚", "辛", "壬", "癸"]
        self.tiangan_yang = ["甲", "丙", "戊", "庚", "壬"]
        self.tiangan_ying = ["乙", "丁", "己", "辛", "癸"]

        self.dizhi_yang = ["子", "寅", "辰", "午", "申", "戌"]
        self.dizhi_ying = ["丑", "卯", "巳", "未", "酉", "亥"]

        self.comboBox_nianzhu_tiangan.addItems(self.tiangan)
        self.comboBox_nianzhu_dizhi.addItems(self.dizhi_yang)
        self.comboBox_yuezhu_tiangan.addItems(self.tiangan)
        self.comboBox_yuezhu_dizhi.addItems(self.dizhi_yang)
        self.comboBox_rizhu_tiangan.addItems(self.tiangan)
        self.comboBox_rizhu_dizhi.addItems(self.dizhi_yang)
        self.comboBox_shizhu_tiangan.addItems(self.tiangan)
        self.comboBox_shizhu_dizhi.addItems(self.dizhi_yang)

        # 天干会影响地支的联动
        self.comboBox_nianzhu_tiangan.currentTextChanged.connect(self.on_tianagan_changed)
        self.comboBox_yuezhu_tiangan.currentTextChanged.connect(self.on_tianagan_changed)
        self.comboBox_rizhu_tiangan.currentTextChanged.connect(self.on_tianagan_changed)
        self.comboBox_shizhu_tiangan.currentTextChanged.connect(self.on_tianagan_changed)

        self.load_data()

    # 天干发生了变化
    def on_tianagan_changed(self):
        # 获取发送信号的控件对象
        sender = self.sender()

        if sender is None:
            return

        # # 方法1：通过对象名识别（推荐，更直观）
        # widget_name = sender.objectName()
        #
        # 方法2：通过直接比较对象识别（适用于未设置对象名的情况）
        trigger_widget = None
        if sender == self.comboBox_nianzhu_tiangan:
            trigger_widget = self.comboBox_nianzhu_dizhi
        elif sender == self.comboBox_yuezhu_tiangan:
            trigger_widget = self.comboBox_yuezhu_dizhi
        elif sender == self.comboBox_rizhu_tiangan:
            trigger_widget = self.comboBox_rizhu_dizhi
        elif sender == self.comboBox_shizhu_tiangan:
            trigger_widget = self.comboBox_shizhu_dizhi

        if trigger_widget is None:
            return

        trigger_widget.clear()
        trigger_widget.addItems(GanZhiYinYang.get_matching_dizhi(sender.currenData()))

    def on_gender_changed(self):
        self.gender = self.comboBox_gender.currentIndex  # 0-男 1-女

    # 信息来源方式发生了变化
    def on_inputinfo_changed(self):
        isInfoInputTimeNotBazi = (self.comboBox_borntime.currentIndex() == 0)
        if isInfoInputTimeNotBazi:  # 输入出生时间和地支
            self.set_layout_enabled(self.verticalLayout_chushengshijian, True)
            self.set_layout_enabled(self.horizontalLayout_tiangan, False)
        else:
            self.set_layout_enabled(self.verticalLayout_chushengshijian, False)
            self.set_layout_enabled(self.horizontalLayout_tiangan, True)

    # 设置控件不可用状态
    def set_layout_enabled(self, layout, enabled):
        """
        设置布局中所有控件的启用/禁用状态

        参数:
            layout: 目标布局
            enabled: True为启用，False为禁用
        """
        if layout is None:
            return

        # 遍历布局中的所有项目
        for i in range(layout.count()):
            item = layout.itemAt(i)

            # 如果是控件
            if item.widget():
                item.widget().setEnabled(enabled)
            # 如果是子布局（递归处理）
            elif item.layout():
                self.set_layout_enabled(item.layout(), enabled)

    def on_solar_lunar_changed(self):
        # 月日要变化,年份不变
        solarOrlunar = self.comboBox_yangliyingli.currentText()
        self.comboBox_yue.clear()
        self.comboBox_ri.clear()

        # // 阻止Combo2发送信号
        self.comboBox_yue.blockSignals(True);
        self.comboBox_ri.blockSignals(True);

        yearNow = self.comboBox_year.currentText()
        daysInMonth = 0
        if solarOrlunar == "农历":
            lunarYear = LunarYear.fromYear(int(yearNow))
            months = lunarYear.getMonthsInYear()
            # if months.count() > 12:#有闰月
            #     leapmonth = lunarYear.getLeapMonth()
            for month in months:
                # self.comboBox_yue.addItem(month.toString())
                parts = month.toString().split('年')  # 分割为 ["1905", "五月(29天)"]
                # month_part = parts[1].split('(')[0]  # 提取 "五月"
                self.comboBox_yue.addItem(parts[1])

            daysInMonth = LunarMonth.fromYm(int(yearNow), 1).getDayCount()
        else:
            for n in range(1, 13):  # 显示12个月的
                self.comboBox_yue.addItem(str(n))
            daysInMonth = 31

        for n in range(1, daysInMonth + 1):
            self.comboBox_ri.addItem(str(n))

        # // 恢复信号发送
        self.comboBox_yue.blockSignals(False)
        self.comboBox_ri.blockSignals(False)

    def btn_OK_clicked(self):
        name_str = self.lineEdit_name.text()
        if name_str is None:
            QMessageBox.critical(self, "错误", "姓名不能为空！")
            return

        #获取设置的地区信息
        self.on_xian_changed(self.comboBox_xian.currentText())
        if self.jd is None:
            QMessageBox.critical(self, "错误", "请设置出生地址！")
            #说明用户没有选择，那就用默认值
            return

        isInfoFromTime = (self.comboBox_borntime.currentIndex() == 0)
        #此时应该进行真太阳时的转换
        timeOffset = calculate_time_offset(float(self.jd))
        if self.comboBox_year:
            text_str = self.comboBox_year.currentText()
            print(text_str)

        bjTime = datetime(int(self.comboBox_year.currentText()),int(self.comboBox_yue.currentText()),
                          int(self.comboBox_ri.currentText()),
                          int(self.comboBox_hour.currentText()),
                          int(self.comboBox_feng.currentText()),int(self.comboBox_miao.currentText()))
        trueTime = datetime_add_minutes(bjTime.strftime("%Y-%m-%d %H:%M:%S"),timeOffset)
        print("函数返回的datetime对象:",trueTime.strftime("%Y-%m-%d %H:%M:%S"))


        # 此时已经获取到经纬度信息了
        # 根据经纬度计算真太阳时
        print(f"btn_taiyangshi_clicked-----jd={self.jd},wd={self.wd}")

        # //solar = Solar(1987, 2, 2, 21, 30, 0)
        solar = Solar(trueTime.year, trueTime.month, trueTime.day, trueTime.hour, trueTime.minute, trueTime.second)
        lunar = solar.getLunar()
        baZi = lunar.getEightChar()
        print(baZi.getYear() + ' ' + baZi.getMonth() + ' ' + baZi.getDay() + ' ' + baZi.getTime())

        gender_str = self.comboBox_gender.currentData()

        year_is_solar_not_lunar = False
        if self.comboBox_borntime.currentIndex == 0:
            # 出生时间
            if self.comboBox_yangliyingli.currentIndex() == 0:
                year_is_solar_not_lunar = True
        else:
            year_is_solar_not_lunar = False

        isTruesolar = self.checkBox_truesolar.isChecked()
        gender_str = self.comboBox_gender.currentText()

        # //传递给下一个页面并显示
        """打开模态对话框并传递参数"""
        # 准备要传递的参数
        baziDetail = BaZiDetail(
            name=name_str,
            gender=gender_str,
            year_is_solar_not_lunar=True,
            year=str(trueTime.year),
            month=str(trueTime.month),
            day=str(trueTime.day),
            hour=str(trueTime.hour),
            minute=str(trueTime.minute),
            second=str(trueTime.second),
            province=self.comboBox_sheng.currentText(),
            city=self.comboBox_shi.currentText(),
            distinct=self.comboBox_xian.currentText(),
            truesolar=isTruesolar,
            zaowanzishi=False
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
        solarOrlunar = self.comboBox_yangliyingli.currentText()
        self.comboBox_yue.clear()

        yearNow = self.comboBox_year.currentText()
        if solarOrlunar == "农历":
            lunarYear = LunarYear.fromYear(int(yearNow))
            months = lunarYear.getMonthsInYear()
            # if months.count() > 12:#有闰月
            #     leapmonth = lunarYear.getLeapMonth()
            for month in months:
                # self.comboBox_yue.addItem(month.toString())
                parts = month.toString().split('年')  # 分割为 ["1905", "五月(29天)"]
                # month_part = parts[1].split('(')[0]  # 提取 "五月"
                self.comboBox_yue.addItem(parts[1])
        else:
            for n in range(1, 13):  # 显示12个月的
                self.comboBox_yue.addItem(str(n))

    def on_month_changed(self):
        solarOrlunar = self.comboBox_yangliyingli.currentText()
        self.comboBox_ri.clear()

        # // 阻止Combo2发送信号
        self.comboBox_ri.blockSignals(True)

        yearNow = self.comboBox_year.currentText()
        monthIndex = self.comboBox_yue.currentIndex()
        monthName = self.comboBox_yue.currentText()
        if monthIndex < 0:
            return

        if solarOrlunar == "农历":
            lunarYear = LunarYear.fromYear(int(yearNow))
            if lunarYear.getLeapMonth() == 0:  # 没有闰月
                daysInMonth = LunarMonth.fromYm(int(yearNow), monthIndex + 1).getDayCount()
                for n in range(1, daysInMonth + 1):
                    self.comboBox_ri.addItem(str(n))
            else:
                lunarMonth = self.lunar_month_to_num(monthName)
                if -1 != monthName.find('闰'):
                    # days = LunarUtil.getDaysOfMonth(int(yearNow, -lunarMonth))
                    days = LunarMonth.fromYm(int(yearNow), -lunarMonth).getDayCount()
                else:
                    # days = LunarUtil.getDaysOfMonth(int(yearNow, lunarMonth))
                    days = LunarMonth.fromYm(int(yearNow), lunarMonth).getDayCount()

            for n in range(1, days + 1):
                self.comboBox_ri.addItem(str(n))
        else:
            # 是否闰月？闰月2月29天
            if SolarUtil.isLeapYear(int(yearNow)):
                if monthIndex == 1:
                    for n in range(1, 30):
                        self.comboBox_ri.addItem(str(n))
        for n in range(1, SolarUtil.getDaysOfMonth(int(yearNow), monthIndex + 1) + 1):
            self.comboBox_ri.addItem(str(n))
        # pass

        # // 恢复信号发送
        self.comboBox_ri.blockSignals(False)

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

    def on_xian_changed(self, district_name):
        print("on_xian_changed,district_name=" + district_name)

        # 获取当前选中的省份
        if not self.comboBox_shi or self.comboBox_shi.currentIndex() < 0:
            print("self.comboBox_shi is null")
            return

        print("on_xian_changed,000" + self.comboBox_shi.currentText())
        city = self.comboBox_shi.currentData()
        # print("on_xian_changed,city=" + city)

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
            self.comboBox_sheng.clear()
            for province in self.data.get('provinces', []):
                self.comboBox_sheng.addItem(province['name'], province)

        except FileNotFoundError:
            QMessageBox.critical(self, "错误", "未找到行政区划数据文件！")
        except json.JSONDecodeError:
            QMessageBox.critical(self, "错误", "行政区划数据文件格式错误！")
        except Exception as e:
            QMessageBox.critical(self, "错误", f"加载数据时发生未知错误：{str(e)}")

    def on_province_changed(self, province_name):
        """省份选择变化时更新城市下拉框"""
        if not self.data or province_name == "":
            return

        # // 阻止Combo2发送信号
        self.comboBox_shi.blockSignals(True)
        self.comboBox_xian.blockSignals(True)

        # 找到选中的省份数据
        for province in self.data.get('provinces', []):
            if province['name'] == province_name:
                # 清空城市和区县下拉框
                self.comboBox_shi.clear()
                self.comboBox_xian.clear()

                # 更新城市下拉框
                for city in province.get('cities', []):
                    self.comboBox_shi.addItem(city['name'], city)
                break

        print(self.comboBox_shi.currentText())

        # 更新区县下拉框
        for city in province.get('cities', []):
            if city['name'] == self.comboBox_shi.currentText():
                for district in city.get('counties', []):
                    self.comboBox_xian.addItem(district['name'],district)
                break
            break

        self.comboBox_shi.blockSignals(False)
        self.comboBox_xian.blockSignals(False)

    def on_city_changed(self, city_name):
        """城市选择变化时更新区县下拉框"""
        if not self.data or self.comboBox_sheng.currentIndex() < 0:
            return

        # 获取当前选中的省份
        province = self.comboBox_sheng.currentData()

        self.comboBox_xian.blockSignals(True)

        # 找到选中的城市数据
        for city in province.get('cities', []):
            if city['name'] == city_name:
                # 清空区县下拉框
                self.comboBox_xian.clear()

                # 更新区县下拉框
                for district in city.get('counties', []):
                    self.comboBox_xian.addItem(district['name'])
                break

        self.comboBox_xian.blockSignals(False)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UserInfoWindow()
    window.show()
    sys.exit(app.exec_())
