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
class LiunianDetail:
    start_year: str
    # age: str
    ganzhi: str#干支名称
    ganzhi_shishen: str#干支十神名称
    rizhi_shiergong: str#相对于日支的十二宫
    nayin: str#此干支的纳音
    kongwang: str#此干支的空亡
    liunian_index: int#大运的索引号，从0开始

    def __init__(self):
        self.start_year = ""
        # self.age = ""
        self.ganzhi = ""
        self.ganzhi_shishen = ""
        self.rizhi_shiergong = ""
        self.nayin = ""
        self.kongwang = ""
        self.liunian_index = 0

    def printData(self):
        print(f"printData:流年[{self.start_year}年---{self.ganzhi}---{self.ganzhi_shishen}"
              f"---{self.rizhi_shiergong}---{self.nayin}---{self.kongwang}")


# 按照 问真八字 页面进行设计排版
class LiunianWidget(QWidget):
    """自定义多文本显示部件"""

    def __init__(self, liunianDetail: LiunianDetail, parent=None):
        super().__init__(parent)

        self.liunianDetail = liunianDetail
        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)

        # -------------------是否开始起运?---------------------------
        is_start_qiyun = False

        if liunianDetail.ganzhi:  # 不为空
            # for item_data in text_items:
            #     self.add_text_item(item_data)
            self.label_start_year = QLabel(liunianDetail.start_year)
            # self.label_age = QLabel(daYunDetail.age)
            self.label_start_year.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # self.label_age.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            self.main_layout.addWidget(self.label_start_year)
            # self.main_layout.addWidget(self.label_age)

            hLayout = QHBoxLayout()
            self.label_liunian_ganzhi = VerticalTextLabel(liunianDetail.ganzhi)
            self.label_shishen_ganzhi = VerticalTextLabel(liunianDetail.ganzhi_shishen)
            hLayout.addWidget(self.label_liunian_ganzhi)
            hLayout.addWidget(self.label_shishen_ganzhi)

            # self.label_shiergong = QLabel(daYunDetail.rizhi_shiergong)
            # self.label_shiergong.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # self.label_nayin = QLabel(daYunDetail.nayin)
            # self.label_nayin.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            # self.label_kongwang = QLabel(daYunDetail.kongwang)
            # self.label_kongwang.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)


            self.main_layout.addLayout(hLayout)

            # self.main_layout.addWidget(self.label_shiergong)
            # self.main_layout.addWidget(self.label_nayin)
            # self.main_layout.addWidget(self.label_kongwang)

        else:
            hLayout = QHBoxLayout()
            self.label_liunian_ganzhi = VerticalTextLabel("流年")
            hLayout.addWidget(self.label_liunian_ganzhi)
            self.main_layout.addLayout(hLayout)

        self.setLayout(self.main_layout)

    def get_liunian_data(self):
        return self.liunianDetail


class LiunianTableHandler:
    """表格处理工具类，用于操作从UI加载的表格"""

    @staticmethod
    def set_text_cell(table_widget, row, col, liunianDetail: LiunianDetail):
        """给表格单元格设置多文本内容"""
        if not isinstance(table_widget, QTableWidget):
            raise ValueError("传入的不是QTableWidget对象")

        widget = LiunianWidget(liunianDetail)
        table_widget.setCellWidget(row, col, widget)

    @staticmethod
    def setup_auto_resize(table_widget):
        """设置表格自动调整大小和平均分配行列"""

        # 关键：隐藏横向表头（列标题）和纵向表头（行标题）
        table_widget.horizontalHeader().hide()  # 隐藏横向表头
        table_widget.verticalHeader().hide()    # 隐藏纵向表头

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
        table_widget.setMinimumSize(400, 150)

        # 让表格随窗口大小变化自动调整
        table_widget.setSizePolicy(
            table_widget.sizePolicy().Expanding,
            table_widget.sizePolicy().Expanding
        )
