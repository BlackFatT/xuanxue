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
class LiuyueDetail:
    jie_date: str  # 节的日期(阳历)
    jie_name: str  # 节的名称

    ganzhi: str  # 干支名称
    ganzhi_shishen: str  # 干支十神名称
    # rizhi_shiergong: str  # 相对于日支的十二宫
    # nayin: str  # 此干支的纳音
    # kongwang: str  # 此干支的空亡
    liuyue_index: int  # 六月的索引号，从0开始,0-11

    def __init__(self):
        self.jie_date = ""
        self.jie_name = ""
        self.ganzhi = ""
        self.ganzhi_shishen = ""
        # self.rizhi_shiergong = ""
        # self.nayin = ""
        # self.kongwang = ""
        liuyue_index = 0

    def printData(self):
        print(f"\n printData:流月[{self.jie_name}---{self.jie_date}")


# 按照 问真八字 页面进行设计排版
class LiuyueWidget(QWidget):
    """自定义多文本显示部件"""

    def __init__(self, liuyueDetail: LiuyueDetail, parent=None):
        super().__init__(parent)

        self.liuyueDetail = liuyueDetail
        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(2, 2, 2, 2)
        self.main_layout.setSpacing(8)

        if liuyueDetail.ganzhi:  # 不为空
            self.jie_name = QLabel(liuyueDetail.jie_name)
            self.jie_name.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            self.jie_date = QLabel(liuyueDetail.jie_date)
            self.jie_date.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

            self.main_layout.addWidget(self.jie_name)
            self.main_layout.addWidget(self.jie_date)

            hLayout = QHBoxLayout()
            self.label_liuyue_ganzhi = VerticalTextLabel(liuyueDetail.ganzhi)
            self.label_liuyue_ganzhi_shishen = VerticalTextLabel(liuyueDetail.ganzhi_shishen)
            hLayout.addWidget(self.label_liuyue_ganzhi)
            hLayout.addWidget(self.label_liuyue_ganzhi_shishen)

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

        # else:
        #     hLayout = QHBoxLayout()
        #     self.label_xiaoyun_ganzhi = VerticalTextLabel("小运")
        #     hLayout.addWidget(self.label_xiaoyun_ganzhi)
        #     self.main_layout.addLayout(hLayout)

        self.setLayout(self.main_layout)

    def get_liuyue_data(self):
        return self.liuyueDetail


class LiuYueTableHandler:
    """表格处理工具类，用于操作从UI加载的表格"""

    @staticmethod
    def set_text_cell(table_widget, row, col, liuyueDetail: LiuyueDetail):
        """给表格单元格设置多文本内容"""
        if not isinstance(table_widget, QTableWidget):
            raise ValueError("传入的不是QTableWidget对象")

        widget = LiuyueWidget(liuyueDetail)
        table_widget.setCellWidget(row, col, widget)

    @staticmethod
    def setup_auto_resize(table_widget):
        """设置表格自动调整大小和平均分配行列"""

        # 关键：隐藏横向表头（列标题）和纵向表头（行标题）
        table_widget.horizontalHeader().hide()  # 隐藏横向表头
        table_widget.verticalHeader().hide()  # 隐藏纵向表头

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
