# 模态对话框类（第二个页面）
from dataclasses import dataclass

# 正确的导入方式
from PyQt5.QtCore import Qt

from PyQt5.QtGui import QColor, QFont, QKeySequence
from PyQt5.QtWidgets import QDialog, QTableWidget, QLabel, QMainWindow, QApplication, QAction, QMessageBox
from PyQt5.uic import loadUi
from lunar_python import Solar, Lunar
from lunar_python.eightchar import Yun

import ganzhi_extractor
from DayunTableHandler import TextItemData, DaYunDetail, DayunTableHandler, DaYunWidget
from LiuYueTableHandler import LiuYueTableHandler, LiuyueDetail
from LiunianTableHandler import LiunianDetail, LiunianTableHandler, LiunianWidget
from XiaoYunTableHandler import XiaoyunDetail, XiaoYunTableHandler, XiaoyunWidget
from shishen import calculate_tiangan_shishen, calculate_dizhi_shishen, calculate_empty_death, get_nayin, \
    get_changsheng12gong, shortening_shishen_name, calculate_ganzhi_shishen, get_element_color, get_jie_name, \
    count_wuxing_fullstring

#常量定义
STABLE_COLUMN_COUNT=10
STABLE_ROW_COUNT=1

#流月表-1-12
STABLE_LIUYUE_COLUMN_COUNT=12
STABLE_LIUYUE_ROW_COUNT=1


@dataclass
class BaZiDetail:
    name: str
    gender: str
    year_is_solar_not_lunar: bool
    # year_solar_all: str
    # year_lunar_all: str
    year: str
    month: str
    day: str
    hour: str
    minute: str
    second: str
    province: str
    city: str
    distinct: str
    truesolar: bool
    zaowanzishi: bool


# 扩展：更丰富的五行颜色方案（包含备选色）
FIVE_ELEMENTS_COLORS_EXTENDED = {
    '金': {'primary': '#FFFFFF', 'secondary': '#FFD700'},  # 白色、金色
    '木': {'primary': '#008000', 'secondary': '#228B22'},  # 绿色、森林绿
    '水': {'primary': '#0000FF', 'secondary': '#00008B'},  # 蓝色、深蓝色
    '火': {'primary': '#FF0000', 'secondary': '#FF4500'},  # 红色、橙红色
    '土': {'primary': '#A52A2A', 'secondary': '#D2691E'}  # 棕色、赭石色
}


def set_label_style(label, bg_color, text_color, font_size):
    """
    使用样式表设置Label样式
    :param label: QLabel实例
    :param bg_color: 背景色RGB元组，如(255,215,0)
    :param text_color: 字体颜色RGB元组，如(255,255,255)
    :param font_size: 字体大小
    """
    # 转换RGB元组为样式表格式
    bg_str = f"rgb{bg_color}"
    text_str = f"rgb{text_color}"

    # 统一设置样式表（背景、字体大小、字体颜色）
    label.setStyleSheet(f"""
        background-color: {bg_str};
        color: {text_str};
        font-size: {font_size}px;
        font-weight: bold;  # 可选：加粗
        padding: 8px;       # 可选：内边距，让内容不贴边
        border-radius: 4px; # 可选：圆角边框
    """)
    # 设置文本居中（可选）
    label.setAlignment(Qt.AlignCenter)


class BaziDialog(QMainWindow):
    def __init__(self, params: BaZiDetail, parent=None):
        super().__init__(parent)  # 继承QDialog
        self.table_liuyue = None
        self.ganzhi_label_list = None
        self.selDayunData = None

        self.daYunArr = None
        self.yun = None
        self.table_dayun = None
        self.baZi = None
        self.lunar = None
        self.solar = None
        self.params = params  # 接收传递的参数
        self.init_ui()

    def getFullDateTimeString(self, year: str, month: str, day: str, hour: str, minute: str):
        return year + "-" + month + "-" + day + "  " + hour + ":" + minute;

    def getFullTimeString(self, hour: str, minute: str):
        return "  " + hour + ":" + minute;

    def init_table(self):
        self.table_dayun = self.findChild(QTableWidget, "tableWidget_dayun")
        if self.table_dayun == None:
            print("未找到表格部件，请检查UI文件中的对象名")
            return

        self.table_liunian = self.findChild(QTableWidget, "tableWidget_liunian")
        if self.table_liunian == None:
            print("未找到表格部件，请检查UI文件中的对象名")
            return

        self.table_xiaoyun = self.findChild(QTableWidget, "tableWidget_xiaoyun")
        if self.table_xiaoyun == None:
            print("未找到表格部件，请检查UI文件中的对象名")
            return

        self.table_liuyue = self.findChild(QTableWidget, "tableWidget_liuyue")
        if self.table_liuyue is None:
            print("未找到表格部件，请检查UI文件中的对象名")
            return

        # 设置自动调整大小
        DayunTableHandler.setup_auto_resize(self.table_dayun)
        # # # 动态设置行列数（如果需要）
        self.table_dayun.setRowCount(STABLE_ROW_COUNT)  # 设置为5行
        self.table_dayun.setColumnCount(STABLE_COLUMN_COUNT)  # 设置为3列
        # dayun_tableheader = DaYunDetail()#设置第一列，没有具体数据
        # CustomTableHandler.set_text_cell(self.table_dayun, 0, 0, dayun_tableheader)
        self.table_dayun.cellClicked.connect(self.on_cell_clicked_dayun)

        # 流年
        # 设置自动调整大小
        LiunianTableHandler.setup_auto_resize(self.table_liunian)
        self.table_liunian.setRowCount(STABLE_ROW_COUNT)  # 设置为5行
        self.table_liunian.setColumnCount(STABLE_COLUMN_COUNT)  # 设置为3列
        # liunian_tableheader = LiunianDetail()  # 设置第一列，没有具体数据
        # LiunianTableHandler.set_text_cell(self.table_liunian, 0, 0, liunian_tableheader)
        self.table_liunian.cellClicked.connect(self.on_cell_clicked_liunian)

        # 小运
        # 设置自动调整大小
        XiaoYunTableHandler.setup_auto_resize(self.table_xiaoyun)
        self.table_xiaoyun.setRowCount(STABLE_ROW_COUNT)  # 设置为5行
        self.table_xiaoyun.setColumnCount(STABLE_COLUMN_COUNT)  # 设置为3列
        xiaoyun_tableheader = XiaoyunDetail()  # 设置第一列，没有具体数据
        XiaoYunTableHandler.set_text_cell(self.table_xiaoyun, 0, 0, xiaoyun_tableheader)
        self.table_xiaoyun.cellClicked.connect(self.on_cell_clicked_xiaoyun)

        # 流月
        # 设置自动调整大小
        LiuYueTableHandler.setup_auto_resize(self.table_liuyue)
        self.table_liuyue.setRowCount(STABLE_LIUYUE_ROW_COUNT)
        self.table_liuyue.setColumnCount(STABLE_LIUYUE_COLUMN_COUNT)
        # self.table_xiaoyun.cellClicked.connect(self.on_cell_clicked_xiaoyun)

        # // 获取大运表
        self.daYunArr = self.yun.getDaYun()
        for i in range(len(self.daYunArr)):
            dayunDetail = DaYunDetail()
            da_yun = self.daYunArr[i]
            dayunDetail.start_year = str(da_yun.getStartYear())
            dayunDetail.age = str(da_yun.getStartAge()) + "岁"
            dayunDetail.ganzhi = da_yun.getGanZhi()
            dayunDetail.dayun_index = i
            if dayunDetail.ganzhi:  # 不等于空
                dayunDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], dayunDetail.ganzhi)
                dayunDetail.rizhi_shiergong = get_changsheng12gong(self.baZi.getDay()[0], dayunDetail.ganzhi[1])
                dayunDetail.kongwang = calculate_empty_death(dayunDetail.ganzhi)
                dayunDetail.nayin = get_nayin(dayunDetail.ganzhi)
                if self.selDayunData is None:
                    self.selDayunData = dayunDetail
            # print(f"大运[{i}] = {da_yun.getStartYear()}年 {da_yun.getStartAge()}岁 {da_yun.getGanZhi()}")
            # dayunDetail = DaYunDetail(str(da_yun.getStartYear()), str(da_yun.getStartAge())+"岁",
            #                           da_yun.getGanZhi(), calculate_ganzhi_shishen(self.baZi.getDay()[0],da_yun.getGanZhi()))
            DayunTableHandler.set_text_cell(self.table_dayun, 0, i, dayunDetail)

        # // 设置第1次大运所在的流年(均为有效数据)
        # liuNianArr = daYunArr[1].getLiuNian()
        self.setLiuNianTableData(1)
        # for i in range(len(liuNianArr)):
        #     liunianDetail = LiunianDetail()
        #     liunian = liuNianArr[i]
        #     liunianDetail.start_year = str(liunian.getYear())
        #     liunianDetail.ganzhi = liunian.getGanZhi()
        #     liunianDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], liunianDetail.ganzhi)
        #     LiunianTableHandler.set_text_cell(self.table_liunian, 0, i + 1, liunianDetail)

        # // 设置第1次大运所在的小运(均为有效数据)
        # xiaoyunArr = self.daYunArr[1].getXiaoYun()
        # xiaoyunDetail = XiaoyunDetail()
        # for i in range(len(xiaoyunArr)):
        #     xiaoyun = xiaoyunArr[i]
        #     xiaoyunDetail.start_year = str(xiaoyun.getYear())
        #     xiaoyunDetail.ganzhi = xiaoyun.getGanZhi()
        #     xiaoyunDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], xiaoyunDetail.ganzhi)
        #     XiaoYunTableHandler.set_text_cell(self.table_xiaoyun, 0, i + 1, xiaoyunDetail)
        self.setXiaoYunTableData(1)

        self.setLiuYueTableData(str(self.daYunArr[1].getXiaoYun()[0].getYear()))

    # 根据大运和流年索引号获取流年详细的信息
    def getLiunianFromDayun(self, dayunIndex, liunianIndex):
        liuNianArray = self.daYunArr[dayunIndex].getLiuNian()
        if liuNianArray is None:
            return

        liunianDetail = LiunianDetail()
        liunian = liuNianArray[liunianIndex]
        liunianDetail.start_year = str(liunian.getYear())
        liunianDetail.ganzhi = liunian.getGanZhi()
        liunianDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], liunianDetail.ganzhi)

        liunianDetail.rizhi_shiergong = get_changsheng12gong(self.baZi.getDay()[0], liunianDetail.ganzhi[1])
        liunianDetail.kongwang = calculate_empty_death(liunianDetail.ganzhi)
        liunianDetail.nayin = get_nayin(liunianDetail.ganzhi)

        #流月
        # liuyueInfo = liuNianArray[liunianIndex].getLiuYue()

        return liunianDetail

    # 根据大运和流年索引号获取流年详细的信息
    def getXiaoyunFromDayun(self, dayunIndex, xiaoyunIndex):
        xiaoyunArray = self.daYunArr[dayunIndex].getXiaoYun()
        if xiaoyunArray is None:
            return

        xiaoyunDetail = XiaoyunDetail()
        xiaoyun = xiaoyunArray[xiaoyunIndex]
        xiaoyunDetail.start_year = str(xiaoyun.getYear())
        xiaoyunDetail.ganzhi = xiaoyun.getGanZhi()
        xiaoyunDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], xiaoyunDetail.ganzhi)

        xiaoyunDetail.rizhi_shiergong = get_changsheng12gong(self.baZi.getDay()[0], xiaoyunDetail.ganzhi[1])
        xiaoyunDetail.kongwang = calculate_empty_death(xiaoyunDetail.ganzhi)
        xiaoyunDetail.nayin = get_nayin(xiaoyunDetail.ganzhi)

        return xiaoyunDetail

    # 设置流年表格中的数据内容
    def setLiuNianTableData(self, dayunIndex):
        liuNianArray = self.daYunArr[dayunIndex].getLiuNian()
        if liuNianArray is None:
            return

        self.clear_cellwidget_table(self.table_liunian)

        # liunian_tableheader = LiunianDetail()  # 设置第一列，没有具体数据
        # LiunianTableHandler.set_text_cell(self.table_liunian, 0, 0, liunian_tableheader)

        for i in range(len(liuNianArray)):
            liunianDetail = LiunianDetail()
            liunian = liuNianArray[i]
            liunianDetail.liunian_index = i
            liunianDetail.start_year = str(liunian.getYear())
            liunianDetail.ganzhi = liunian.getGanZhi()
            liunianDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], liunianDetail.ganzhi)

            liunianDetail.rizhi_shiergong = get_changsheng12gong(self.baZi.getDay()[0], liunianDetail.ganzhi[1])
            liunianDetail.kongwang = calculate_empty_death(liunianDetail.ganzhi)
            liunianDetail.nayin = get_nayin(liunianDetail.ganzhi)

            LiunianTableHandler.set_text_cell(self.table_liunian, 0, i, liunianDetail)

    # 设置小运表格中的数据内容
    def setXiaoYunTableData(self, dayunIndex):
        xiaoyunArray = self.daYunArr[dayunIndex].getXiaoYun()
        if xiaoyunArray is None:
            return

        self.clear_cellwidget_table(self.table_xiaoyun)

        # xiaoyun_tableheader = XiaoyunDetail()  # 设置第一列，没有具体数据
        # XiaoYunTableHandler.set_text_cell(self.table_xiaoyun, 0, 0, xiaoyun_tableheader)

        for i in range(len(xiaoyunArray)):
            xiaoyunDetail = XiaoyunDetail()
            xiaoyun = xiaoyunArray[i]
            xiaoyunDetail.xiaoyun_index = i
            xiaoyunDetail.start_year = str(xiaoyun.getYear())
            xiaoyunDetail.ganzhi = xiaoyun.getGanZhi()
            xiaoyunDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], xiaoyunDetail.ganzhi)

            xiaoyunDetail.rizhi_shiergong = get_changsheng12gong(self.baZi.getDay()[0], xiaoyunDetail.ganzhi[1])
            xiaoyunDetail.kongwang = calculate_empty_death(xiaoyunDetail.ganzhi)
            xiaoyunDetail.nayin = get_nayin(xiaoyunDetail.ganzhi)

            XiaoYunTableHandler.set_text_cell(self.table_xiaoyun, 0, i, xiaoyunDetail)

    # 设置流月表格中的数据内容,根据年份来调整,输入年份和在大运中的索引
    def setLiuYueTableData(self, year:str,yearinDaYunIndex=0,dayunIndex=1):
        if int(year) >= 3000 or int(year) <= 1000:
            return

        if self.daYunArr is None:
            return

        self.clear_cellwidget_table(self.table_liuyue,STABLE_LIUYUE_ROW_COUNT,STABLE_LIUYUE_COLUMN_COUNT)
        jieqiAll = Lunar.fromYmd(int(year),2,5).getJieQiTable()#后面是按照立春来设置的
        if jieqiAll is None:
            return

        if self.selDayunData:
            dayunIndex = self.selDayunData.dayun_index

        liuNianArray = self.daYunArr[dayunIndex].getLiuNian()
        if liuNianArray is None:
            return

        #流月
        liuyueArray = liuNianArray[yearinDaYunIndex].getLiuYue()
        if liuyueArray is None:
            return

        for i in range(len(liuyueArray)):
            liuyueDetail = LiuyueDetail()
            liuyue = liuyueArray[i]
            liuyueDetail.liuyue_index = i
            liuyueDetail.jie_name = get_jie_name(i)
            liuyueDetail.jie_date = jieqiAll[liuyueDetail.jie_name].toYmdHms()[5:]#去除了年的部分
            liuyueDetail.ganzhi =liuyue.getGanZhi()
            liuyueDetail.ganzhi_shishen = calculate_ganzhi_shishen(self.baZi.getDay()[0], liuyueDetail.ganzhi)

            # xiaoyunDetail.rizhi_shiergong = get_changsheng12gong(self.baZi.getDay()[0], xiaoyunDetail.ganzhi[1])
            # xiaoyunDetail.kongwang = calculate_empty_death(xiaoyunDetail.ganzhi)
            # xiaoyunDetail.nayin = get_nayin(xiaoyunDetail.ganzhi)

            LiuYueTableHandler.set_text_cell(self.table_liuyue, 0, i, liuyueDetail)

        #将“流月”标签后面加上年份
        self.label_liuyue.setText("流月--"+year)

    def init_ui(self):
        # 加载UI文件
        # loadUi("BaziDialog.ui", self)
        loadUi("mainwindow.ui", self)

        self.label_Name_value.setText(self.params.name+"("+self.params.gender+")")
        # self.label_Name.setVisible(False)

        if self.params.year_is_solar_not_lunar:
            # self.label_solar_value.setText(self.params.year_solar_all)
            # self.label_solar_value.setText(
            #     self.getFullTimeString(self.params.year, self.params.month, self.params.day,
            #                            self.params.hour, self.params.minute))
            self.solar = Solar(int(self.params.year), int(self.params.month), int(self.params.day),
                               int(self.params.hour), int(self.params.minute), int(0))
            self.lunar = self.solar.getLunar()
            # self.label_lunar_value.setText(
            #     self.lunar.toString() + self.getFullTimeString(self.params.hour, self.params.minute))
        else:
            # //转换成农历
            # self.label_lunar_value.setText(self.params.year_lunar_all)
            # self.lunar = Lunar.fromYmd(self.params.year, self.params.month, self.params.day)
            self.lunar = Lunar(int(self.params.year), int(self.params.month), int(self.params.day),
                               int(self.params.hour), int(self.params.minute), int(0))
            self.solar = self.lunar.getSolar()

        # //设置日期和时间
        self.label_solar_value.setText(
            self.solar.toString() + self.getFullTimeString(self.params.hour, self.params.minute))
        self.label_lunar_value.setText(
            self.lunar.toString() + self.getFullTimeString(self.params.hour, self.params.minute))

        # solar = Solar(1987, 2, 2, 21, 30, 0)
        # lunar = solar.getLunar()
        self.baZi = self.lunar.getEightChar()
        print(self.baZi.getYear() + ' ' + self.baZi.getMonth() + ' ' + self.baZi.getDay() + ' ' + self.baZi.getTime())

        # //设置天干地支数值
        self.label_tiangan_nianzhu.setText(self.baZi.getYear()[0])
        self.label_dizhi_nianzhu.setText(self.baZi.getYear()[1])
        self.label_tiangan_yuezhu.setText(self.baZi.getMonth()[0])
        self.label_dizhi_yuezhu.setText(self.baZi.getMonth()[1])
        self.label_tiangan_rizhu.setText(self.baZi.getDay()[0])
        self.label_dizhi_rizhu.setText(self.baZi.getDay()[1])
        self.label_tiangan_shizhu.setText(self.baZi.getTime()[0])
        self.label_dizhi_shizhu.setText(self.baZi.getTime()[1])

        # //计算干支的十神
        self.label_zhuxing_nianzhu.setText(calculate_tiangan_shishen(self.baZi.getDay()[0], self.baZi.getYear()[0]))
        self.label_dizhi_zhuxing_nianzhu.setText(calculate_dizhi_shishen(self.baZi.getDay()[0], self.baZi.getYear()[1]))

        self.label_zhuxing_yuezhu.setText(calculate_tiangan_shishen(self.baZi.getDay()[0], self.baZi.getMonth()[0]))
        self.label_dizhi_zhuxing_yuezhu.setText(calculate_dizhi_shishen(self.baZi.getDay()[0], self.baZi.getMonth()[1]))

        self.label_dizhi_zhuxing_rizhu.setText(calculate_dizhi_shishen(self.baZi.getDay()[0], self.baZi.getDay()[1]))

        self.label_zhuxing_shizhu.setText(calculate_tiangan_shishen(self.baZi.getDay()[0], self.baZi.getTime()[0]))
        self.label_dizhi_zhuxing_shizhu.setText(calculate_dizhi_shishen(self.baZi.getDay()[0], self.baZi.getTime()[1]))

        # //空丸
        self.label_kongwang_nianzhu.setText(calculate_empty_death(self.baZi.getYear()))
        self.label_kongwang_yuezhu.setText(calculate_empty_death(self.baZi.getMonth()))
        self.label_kongwang_rizhu.setText(calculate_empty_death(self.baZi.getDay()))
        self.label_kongwang_shizhu.setText(calculate_empty_death(self.baZi.getTime()))

        # //纳音
        self.label_nayin_nianzhu.setText(get_nayin(self.baZi.getYear()))
        self.label_nayin_yuezhu.setText(get_nayin(self.baZi.getMonth()))
        self.label_nayin_rizhu.setText(get_nayin(self.baZi.getDay()))
        self.label_nayin_shizhu.setText(get_nayin(self.baZi.getTime()))

        # //十二宫
        self.label_xingyun_nianzhu.setText(get_changsheng12gong(self.baZi.getDay()[0], self.baZi.getYear()[1]))
        self.label_xingyun_yuezhu.setText(get_changsheng12gong(self.baZi.getDay()[0], self.baZi.getMonth()[1]))
        self.label_xingyun_rizhu.setText(get_changsheng12gong(self.baZi.getDay()[0], self.baZi.getDay()[1]))
        self.label_xingyun_shizhu.setText(get_changsheng12gong(self.baZi.getDay()[0], self.baZi.getTime()[1]))

        # //大运时间设置
        self.yun = self.baZi.getYun(1)
        self.label_qiyun_value.setText(
            "出生" + str(self.yun.getStartYear()) + "年" + str(self.yun.getStartMonth()) + "个月" + str(
                self.yun.getStartDay()) + "天后起运")

        #五行比例
        ganzhi_all = [self.baZi.getYear()[0], self.baZi.getYear()[1], self.baZi.getMonth()[0], self.baZi.getMonth()[1],
                      self.baZi.getDay()[0], self.baZi.getDay()[1], self.baZi.getTime()[0], self.baZi.getTime()[1]]

        self.label_wuxingbili.setText(count_wuxing_fullstring(ganzhi_all))

        #出生地址
        self.label_address.setText(self.params.province+self.params.city+self.params.distinct)

        # 搜集干支显示控件
        self.ganzhi_label_list = []

        self.ganzhi_label_list.append(self.label_tiangan_dayun)
        self.ganzhi_label_list.append(self.label_dizhi_dayun)

        self.ganzhi_label_list.append(self.label_tiangan_liunian)
        self.ganzhi_label_list.append(self.label_dizhi_liunian)

        self.ganzhi_label_list.append(self.label_tiangan_xiaoyun)
        self.ganzhi_label_list.append(self.label_dizhi_xiaoyun)

        self.ganzhi_label_list.append(self.label_tiangan_nianzhu)
        self.ganzhi_label_list.append(self.label_dizhi_nianzhu)

        self.ganzhi_label_list.append(self.label_tiangan_yuezhu)
        self.ganzhi_label_list.append(self.label_dizhi_yuezhu)

        self.ganzhi_label_list.append(self.label_tiangan_rizhu)
        self.ganzhi_label_list.append(self.label_dizhi_rizhu)

        self.ganzhi_label_list.append(self.label_tiangan_shizhu)
        self.ganzhi_label_list.append(self.label_dizhi_shizhu)

        # UI的美化----------------------------------
        # 调用样式设置方法
        self.set_label_style(
            self.label_liunian2,
            bg_color=(100, 0, 0),  # 红色背景
            text_color=(0, 255, 0),  # 绿色字体
            font_size=20
        )

        self.set_label_style(
            self.label_xiaoyun2,
            bg_color=(255, 0, 0),  # 红色背景
            text_color=(0, 255, 0),  # 绿色字体
            font_size=20
        )

        self.set_label_style(
            self.label_dayun2,
            bg_color=(0, 200, 0),  # 红色背景
            text_color=(0, 0, 200),  # 绿色字体
            font_size=20
        )

        self.set_label_style(
            self.label_liuyue,
            bg_color=(0, 200, 0),  # 红色背景
            text_color=(0, 0, 200),  # 绿色字体
            font_size=20
        )
        self.setGanZhiStyle()

        self.init_table()
        self.createMenus()


        self.center_widget()
        # # 使用参数更新界面内容
        # self.title_label.setText(self.params.title)
        # self.info_label.setText(f"内容: {self.params.content}\n来源: {self.params.author}")
        #
        # # 绑定关闭按钮事件
        # self.close_btn.clicked.connect(self.accept)  # 确认关闭，返回Accepted状态
        # # 也可以用self.reject()表示取消关闭，返回Rejected状态


    # 大运 表格被点击的响应函数
    def on_cell_clicked_dayun(self, row, col):
        """单元格单击事件处理函数"""
        # # 获取点击的行、列索引（从0开始）
        # row = item.row()
        # col = item.column()
        # 获取单元格内容
        cell_widget = self.table_dayun.cellWidget(row, col)
        if cell_widget is None:
            return

        if isinstance(cell_widget, DaYunWidget):
            self.selDayunData = cell_widget.get_data()
            self.selDayunData.printData()
        else:
            return

        #判断是否有流年小运的信息？起运之前没有数据的!
        if self.selDayunData.dayun_index == 0 or self.selDayunData.ganzhi == "":
            return

        # # 加载相应的流年和小运信息并显示
        self.setLiuNianTableData(self.selDayunData.dayun_index)
        self.setXiaoYunTableData(self.selDayunData.dayun_index)
        self.setLiuYueTableData(str(self.daYunArr[self.selDayunData.dayun_index].getLiuNian()[0].getYear()))

        self.get_size(self.table_dayun)

        # 此时默认显示第一个流年和小运
        self.set_Dayun_Liunian_Xiaoyun_OnLeftUI(self.selDayunData,
                                                self.getLiunianFromDayun(self.selDayunData.dayun_index, 0),
                                                self.getXiaoyunFromDayun(self.selDayunData.dayun_index, 0))

    def on_cell_clicked_liunian(self, row, col):
        # 获取单元格内容
        cell_widget = self.table_liunian.cellWidget(row, col)
        if cell_widget is None:
            return

        if isinstance(cell_widget, LiunianWidget):
            liunianData = cell_widget.get_liunian_data()
            liunianData.printData()
        else:
            return

        # # 加载相应的流年和小运信息并显示
        # self.setLiuNianTableData(dayunData.dayun_index)
        # self.setXiaoYunTableData(dayunData.dayun_index)
        # if self.selDayunData is None:
        #     #说明之前没有点击选中过大运有效的表格
        #     dayunDetail = self.table_dayun.cellWidget()

        # self.get_size(self.table_liunian)

        if self.selDayunData:
            self.set_Dayun_Liunian_Xiaoyun_OnLeftUI(self.selDayunData, liunianData,
                                                   self.getXiaoyunFromDayun(self.selDayunData.dayun_index,
                                                                            liunianData.liunian_index))
            self.setLiuYueTableData(liunianData.start_year,liunianData.liunian_index,self.selDayunData.dayun_index)

    def on_cell_clicked_xiaoyun(self, row, col):
        # 获取单元格内容
        cell_widget = self.table_xiaoyun.cellWidget(row, col)
        if cell_widget is None:
            return

        if isinstance(cell_widget, XiaoyunWidget):
            xiaoyunData = cell_widget.get_xiaoyun_data()
            xiaoyunData.printData()
        else:
            return

        if self.selDayunData:
            self.set_Dayun_Liunian_Xiaoyun_OnLeftUI(self.selDayunData,
            self.getLiunianFromDayun(self.selDayunData.dayun_index,xiaoyunData.xiaoyun_index),
                                                   xiaoyunData)
            self.setLiuYueTableData(xiaoyunData.start_year,xiaoyunData.xiaoyun_index,self.selDayunData.dayun_index)

    # 清空表格中的内容，防止内存泄漏
    def clear_cellwidget_table(self, yourTableWidget,rowcount=STABLE_ROW_COUNT,columncount=STABLE_COLUMN_COUNT):
        row_count = yourTableWidget.rowCount()
        column_count = yourTableWidget.columnCount()
        if row_count <= 0 or column_count <= 0:
            return

        for row in range(row_count):
            for col in range(column_count):
                # 获取单元格中的Widget
                widget = yourTableWidget.cellWidget(row, col)
                if widget:
                    # 从表格中移除并删除Widget
                    yourTableWidget.setCellWidget(row, col, None)  # 移除关联
                    widget.deleteLater()  # 安全删除，释放内存

        # 重新设置行与列
        yourTableWidget.setRowCount(rowcount)  # 设置为5行
        yourTableWidget.setColumnCount(columncount)  # 设置为3列

    # 改变最左边UI的大运、小运和流年信息的显示内容
    def set_Dayun_Liunian_Xiaoyun_OnLeftUI(self, dayunDetail, liunianDetail, xiaoyunDetail):
        # 大运-天干地支及其主星-星运-空亡-纳音
        self.label_zhuxing_dayun.setText(dayunDetail.ganzhi_shishen[0])
        self.label_tiangan_dayun.setText(dayunDetail.ganzhi[0])

        self.label_dizhi_zhuxing_dayun.setText(dayunDetail.ganzhi_shishen[1])
        self.label_dizhi_dayun.setText(dayunDetail.ganzhi[1])

        self.label_xingyun_dayun.setText(dayunDetail.rizhi_shiergong)
        self.label_kongwang_dayun.setText(dayunDetail.kongwang)
        self.label_nayin_dayun.setText(dayunDetail.nayin)

        # 流年-天干地支及其主星-星运-空亡-纳音
        self.label_zhuxing_liunian.setText(liunianDetail.ganzhi_shishen[0])
        self.label_tiangan_liunian.setText(liunianDetail.ganzhi[0])

        self.label_dizhi_zhuxing_liunian.setText(liunianDetail.ganzhi_shishen[1])
        self.label_dizhi_liunian.setText(liunianDetail.ganzhi[1])

        self.label_xingyun_liunian.setText(liunianDetail.rizhi_shiergong)
        self.label_kongwang_liunian.setText(liunianDetail.kongwang)
        self.label_nayin_liunian.setText(liunianDetail.nayin)

        # 小运-天干地支及其主星-星运-空亡-纳音
        self.label_zhuxing_xiaoyun.setText(xiaoyunDetail.ganzhi_shishen[0])
        self.label_tiangan_xiaoyun.setText(xiaoyunDetail.ganzhi[0])

        self.label_dizhi_zhuxing_xiaoyun.setText(xiaoyunDetail.ganzhi_shishen[1])
        self.label_dizhi_xiaoyun.setText(xiaoyunDetail.ganzhi[1])

        self.label_xingyun_xiaoyun.setText(xiaoyunDetail.rizhi_shiergong)
        self.label_kongwang_xiaoyun.setText(xiaoyunDetail.kongwang)
        self.label_nayin_xiaoyun.setText(xiaoyunDetail.nayin)

        # 根据干支的五行显示不同的颜色-金木水火土
        self.setGanZhiStyle()

    # 设置主页面7个柱位的干支的字体颜色等
    def setGanZhiStyle(self):
        for nowLabel in self.ganzhi_label_list:
            # nowLabel = self.ganzhi_label_list[i]
            if nowLabel:
                # 确保是标签控件（增加类型校验）
                if not hasattr(nowLabel, 'text') or not hasattr(nowLabel, 'setFont'):
                    print(f"警告：列表中包含非标签对象 {nowLabel}，已跳过")
                    continue

                # print(f"text={nowLabel.text().strip()},color={get_element_color(nowLabel.text().strip())}")

                self.setCtrlFont(nowLabel, get_element_color(nowLabel.text().strip()))

    # 设置label控件字体
    def setCtrlFont(self, yourLabel, rgb_color=(0, 0, 0)):
        # 1. 设置字体尺寸和加粗
        font = QFont()
        font.setPointSize(28)  # 字体尺寸
        font.setBold(True)  # 加粗
        font.setFamily("Arial Black")
        yourLabel.setFont(font)

        # 2. 设置颜色（使用样式表）
        # rgb_color: RGB颜色元组，如(255, 0, 0)
        # 校验输入是否为有效的RGB元组
        if isinstance(rgb_color, tuple) and len(rgb_color) == 3:
            # 转换为样式表支持的格式：rgb(r, g, b)
            color_str = f"rgb{rgb_color}"  # 等价于 f"rgb({rgb_color[0]}, {rgb_color[1]}, {rgb_color[2]})"
            yourLabel.setStyleSheet(f"color: {color_str};")
        else:
            print("错误：颜色参数必须是包含3个元素的RGB元组，如(255, 0, 0)")

    def set_label_style(self, label, bg_color, text_color, font_size):
        # 1. 先单独测试文本居中（确认基础功能正常）
        # label.setAlignment(Qt.AlignCenter)

        # 2. 构建完整的样式表字符串（避免拼接错误）
        # 手动拼接RGB格式，确保语法正确
        bg_r, bg_g, bg_b = bg_color
        text_r, text_g, text_b = text_color

        # 完整样式表（用三重引号避免引号冲突）
        style_sheet = f"""
            QLabel {{
                background-color: rgb({bg_r}, {bg_g}, {bg_b}) !important;
                color: rgb({text_r}, {text_g}, {text_b}) !important;
                font-size: {font_size}px !important;
                font-weight: bold !important;
                padding: 10px !important;
                border: 1px solid #000 !important; /* 增加边框辅助观察 */
            }}
        """

        # # 3. 打印样式表（用于调试，确认格式正确）
        # print("应用的样式表：")
        # print(style_sheet)

        # 4. 强制清除现有样式并应用新样式
        label.setStyleSheet("")  # 先清除旧样式
        label.setStyleSheet(style_sheet)

        # 5. 确保没有其他属性干扰
        # label.setFlat(False)  # 禁用flat属性（可能影响背景显示）
        label.setAttribute(Qt.WA_StyledBackground, True)  # 强制启用样式背景

    def center_widget(self):
        """方法1：使用QWidget的moveCenter方法（简洁）"""
        # 确保窗口尺寸已确定
        self.adjustSize()  # 调整窗口至合适大小（可选）

        # 获取屏幕的几何信息（当前屏幕）
        screen_geometry = QApplication.desktop().availableGeometry(self)

        # 计算窗口居中的位置
        window_geometry = self.frameGeometry()
        window_geometry.moveCenter(screen_geometry.center())

        # 移动窗口到计算出的位置
        self.move(window_geometry.topLeft())

    #获取指定控件的此村
    def get_size(self,widget):
        """获取并显示控件的尺寸信息"""
        # widget = self.example_widget

        # 方法1：获取宽度和高度（最常用）
        width = widget.width()
        height = widget.height()

        # 方法2：获取尺寸对象（包含宽高）
        size = widget.size()  # 返回QSize对象
        size_width = size.width()
        size_height = size.height()

        # 方法3：获取包含边框的总尺寸（包括窗口边框等装饰）
        # 注意：对于普通控件，与size()通常相同；对于顶级窗口可能不同
        frame_size = widget.frameSize()
        frame_width = frame_size.width()
        frame_height = frame_size.height()

        # 方法4：获取最小/最大允许尺寸（不是当前尺寸，而是限制值）
        min_size = widget.minimumSize()
        max_size = widget.maximumSize()

        # 显示结果
        result = (
            f"\n------------------------------------"
            f"当前宽度: {width}, 当前高度: {height}\n"
            f"size() 宽高: {size_width}, {size_height}\n"
            f"frameSize() 宽高: {frame_width}, {frame_height}\n"
            f"最小允许尺寸: {min_size.width()}x{min_size.height()}\n"
            f"最大允许尺寸: {max_size.width()}x{max_size.height()}"
        )
        # self.result_label.setText(result)
        print(result)

    def createMenus(self):
        # 1. 获取菜单栏（QMainWindow 自带）
        menubar = self.menuBar

        # 2. 添加菜单（& 后面的字母为 Alt 快捷键）
        file_menu = menubar.addMenu("文件(&F)")
        edit_menu = menubar.addMenu("编辑(&E)")
        help_menu = menubar.addMenu("帮助(&H)")

        # 3. 为文件菜单添加动作
        # 新建动作
        new_action = QAction("新建(&N)", self)
        new_action.setShortcut(QKeySequence.New)  # 标准快捷键 Ctrl+N
        new_action.setStatusTip("创建新文件")
        new_action.triggered.connect(self.on_menu_action)  # 绑定槽函数
        file_menu.addAction(new_action)

        # 打开动作
        open_action = QAction("打开(&O)", self)
        open_action.setShortcut(QKeySequence.Open)  # Ctrl+O
        open_action.setStatusTip("打开现有文件")
        open_action.triggered.connect(self.on_menu_action)
        file_menu.addAction(open_action)

        # 保存动作
        save_action = QAction("保存(&S)", self)
        save_action.setShortcut(QKeySequence.Save)  # Ctrl+S
        save_action.setStatusTip("保存当前文件")
        save_action.triggered.connect(self.on_menu_action)
        file_menu.addAction(save_action)

        # 添加分隔线
        file_menu.addSeparator()

        # 退出动作
        exit_action = QAction("退出(&X)", self)
        exit_action.setShortcut(QKeySequence.Quit)  # Ctrl+Q
        exit_action.setStatusTip("退出应用程序")
        exit_action.triggered.connect(self.on_menu_action)  # 直接连接到窗口关闭
        file_menu.addAction(exit_action)

        # 4. 为编辑菜单添加动作
        undo_action = QAction("撤销(&U)", self)
        undo_action.setShortcut(QKeySequence.Undo)  # Ctrl+Z
        undo_action.setStatusTip("撤销上一步操作")
        undo_action.triggered.connect(self.on_menu_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction("重做(&R)", self)
        redo_action.setShortcut(QKeySequence.Redo)  # Ctrl+Y
        redo_action.setStatusTip("重做操作")
        redo_action.triggered.connect(self.on_menu_action)
        edit_menu.addAction(redo_action)

        # 5. 为帮助菜单添加动作
        about_action = QAction("关于(&A)", self)
        about_action.setStatusTip("显示关于信息")
        about_action.triggered.connect(self.on_menu_action)
        help_menu.addAction(about_action)

    # 槽函数实现
    def on_menu_action(self):
        QMessageBox.information(self, "提示", "该功能待实现!!")