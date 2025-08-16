import sys
from dataclasses import dataclass

from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QTableWidget)
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QColor, QFont, QPainter, QFontMetrics
from PyQt5.uic import loadUi

# 大运的详细信息，此处只显示，不做计算!
from VerticalTextLabel import VerticalTextLabel


@dataclass
class DaYunDetail:
    start_year: str
    age: str
    ganzhi: str#干支名称
    ganzhi_shishen: str#干支十神名称
    rizhi_shiergong: str#相对于日支的十二宫
    nayin: str#此干支的纳音
    kongwang: str#此干支的空亡
    dayun_index: int#大运的索引号，从0开始

    def __init__(self):
        self.start_year = ""
        self.age = ""
        self.ganzhi = ""
        self.ganzhi_shishen = ""
        self.rizhi_shiergong = ""
        self.nayin = ""
        self.kongwang = ""
        dayun_index = 0

    def printData(self):
        print(f"printData:大运[{self.dayun_index}] = {self.start_year}年---{self.age}---{self.ganzhi}")


class TextItemData:
    """存储单个文本片段的数据类"""

    def __init__(self, text, font_size=12, color=None,
                 h_align=Qt.AlignCenter, v_align=Qt.AlignVCenter,
                 orientation=Qt.Horizontal):
        self.text = text
        self.font_size = font_size
        self.color = color if color is not None else QColor(0, 0, 0)
        self.h_align = h_align
        self.v_align = v_align
        self.orientation = orientation


# 按照 问真八字 页面进行设计排版
class DaYunWidget(QWidget):
    """自定义多文本显示部件"""

    def __init__(self, daYunDetail: DaYunDetail, parent=None):
        super().__init__(parent)

        self.daYunDetail = daYunDetail
        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)

        # for item_data in text_items:
        #     self.add_text_item(item_data)
        self.label_start_year = QLabel(daYunDetail.start_year)
        self.label_age = QLabel(daYunDetail.age)
        self.label_start_year.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label_age.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

        self.main_layout.addWidget(self.label_start_year)
        self.main_layout.addWidget(self.label_age)

        # -------------------是否开始起运?---------------------------
        is_start_qiyun = False

        if daYunDetail.ganzhi:  # 不为空
            hLayout = QHBoxLayout()
            self.label_dayun_ganzhi = VerticalTextLabel(daYunDetail.ganzhi)
            self.label_shishen_ganzhi = VerticalTextLabel(daYunDetail.ganzhi_shishen,"#FF0000",12)
            is_start_qiyun = True
            hLayout.addWidget(self.label_dayun_ganzhi)
            hLayout.addWidget(self.label_shishen_ganzhi)

            # self.label_shiergong = QLabel(daYunDetail.rizhi_shiergong)
            # self.label_shiergong.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # self.label_nayin = QLabel(daYunDetail.nayin)
            # self.label_nayin.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # self.label_kongwang = QLabel(daYunDetail.kongwang)
            # self.label_kongwang.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


            self.main_layout.addLayout(hLayout)

            self.label_12gong_kongwang = QLabel(daYunDetail.rizhi_shiergong + "--"+daYunDetail.kongwang)
            self.label_12gong_kongwang.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            self.main_layout.addWidget(self.label_12gong_kongwang)
            # self.main_layout.addWidget(self.label_nayin)
            # self.main_layout.addWidget(self.label_kongwang)

        else:
            hLayout = QHBoxLayout()
            self.label_dayun_ganzhi = VerticalTextLabel("运前")
            hLayout.addWidget(self.label_dayun_ganzhi)
            self.main_layout.addLayout(hLayout)

        # # 1. 设置字体尺寸和加粗
        # font = QFont()
        # font.setPointSize(16)  # 字体尺寸
        # font.setBold(True)  # 加粗
        # self.label_dayun_ganzhi.setFont(font)
        #
        # # 2. 设置颜色（使用样式表）
        # self.label_dayun_ganzhi.setStyleSheet("color: rgb(255, 0, 0);")  # 红色

        self.setLayout(self.main_layout)

    def get_data(self):
        return self.daYunDetail


# class StyledTextWidget(QWidget):
#     """自定义多文本显示部件"""
#
#     def __init__(self, text_items, main_layout=Qt.Vertical, parent=None):
#         super().__init__(parent)
#
#         if main_layout == Qt.Vertical:
#             self.main_layout = QVBoxLayout()
#         else:
#             self.main_layout = QHBoxLayout()
#
#         self.main_layout.setContentsMargins(5, 5, 5, 5)
#         self.main_layout.setSpacing(10)
#
#         for item_data in text_items:
#             self.add_text_item(item_data)
#
#         self.setLayout(self.main_layout)
#
#     def add_text_item(self, item_data):
#         if not isinstance(item_data.color, QColor):
#             item_data.color = QColor(0, 0, 0)
#
#         if item_data.orientation == Qt.Vertical:
#             label = RotatedLabel(item_data.text)
#             label.setMinimumHeight(100)
#         else:
#             label = QLabel(item_data.text)
#
#         font = QFont()
#         font.setPointSize(item_data.font_size)
#         label.setFont(font)
#
#         label.setStyleSheet(
#             f"color: rgb({item_data.color.red()}, {item_data.color.green()}, {item_data.color.blue()});"
#         )
#
#         label.setAlignment(item_data.h_align | item_data.v_align)
#         self.main_layout.addWidget(label)


# class CustomTableHandler:
#     """表格处理工具类，用于操作从UI加载的表格"""
#
#     @staticmethod
#     def set_text_cell(table_widget, row, col, text_items, main_layout=Qt.Vertical):
#         """给表格单元格设置多文本内容"""
#         if not isinstance(table_widget, QTableWidget):
#             raise ValueError("传入的不是QTableWidget对象")
#
#         widget = StyledTextWidget(text_items, main_layout)
#         table_widget.setCellWidget(row, col, widget)

class DayunTableHandler:
    """表格处理工具类，用于操作从UI加载的表格"""

    @staticmethod
    def set_text_cell(table_widget, row, col, daYunDetail: DaYunDetail):
        """给表格单元格设置多文本内容"""
        if not isinstance(table_widget, QTableWidget):
            raise ValueError("传入的不是QTableWidget对象")

        widget = DaYunWidget(daYunDetail)
        table_widget.setCellWidget(row, col, widget)

    @staticmethod
    def setup_auto_resize(table_widget):

        # 关键：隐藏横向表头（列标题）和纵向表头（行标题）
        table_widget.horizontalHeader().hide()  # 隐藏横向表头
        table_widget.verticalHeader().hide()    # 隐藏纵向表头

        """设置表格自动调整大小和平均分配行列"""
        # 表格充满父容器
        table_widget.horizontalHeader().setStretchLastSection(True)
        table_widget.verticalHeader().setStretchLastSection(True)

        # 平均分配列宽
        table_widget.horizontalHeader().setSectionResizeMode(
            table_widget.horizontalHeader().Stretch
        )

        # 平均分配行高
        table_widget.verticalHeader().setSectionResizeMode(
            table_widget.verticalHeader().Stretch
        )

        # 设置表格最小尺寸
        table_widget.setMinimumSize(1080, 180)

        # 让表格随窗口大小变化自动调整
        table_widget.setSizePolicy(
            table_widget.sizePolicy().Expanding,
            table_widget.sizePolicy().Expanding
        )
