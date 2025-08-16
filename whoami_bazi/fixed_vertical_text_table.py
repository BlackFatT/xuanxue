import sys
from PyQt5.QtWidgets import (QApplication, QTableWidget, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel)
from PyQt5.QtCore import Qt, QRect, QPoint
from PyQt5.QtGui import QColor, QFont, QPainter, QFontMetrics


class TextItemData:
    """存储单个文本片段的数据类，支持文本方向设置"""

    def __init__(self, text, font_size=12, color=None,
                 h_align=Qt.AlignCenter, v_align=Qt.AlignVCenter,
                 orientation=Qt.Horizontal):
        self.text = text
        self.font_size = font_size
        self.color = color if color is not None else QColor(0, 0, 0)
        self.h_align = h_align
        self.v_align = v_align
        self.orientation = orientation


class RotatedLabel(QLabel):
    """自定义标签，修复垂直文本显示问题"""

    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.rotation = 90  # 垂直文本旋转90度
        self.setMinimumSize(30, 80)  # 确保有足够的显示空间

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)

        # 保存当前状态
        painter.save()

        # 获取文本尺寸
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()

        # 计算旋转后的位置 - 关键修复
        painter.translate(0, self.height())
        painter.rotate(-self.rotation)  # 使用负角度旋转

        # 绘制文本
        painter.drawText(QPoint(0, text_height), self.text())

        # 恢复状态
        painter.restore()

    def sizeHint(self):
        # 计算适合旋转文本的尺寸
        font_metrics = QFontMetrics(self.font())
        return font_metrics.size(Qt.TextSingleLine, self.text()).transposed()


class StyledTextWidget(QWidget):
    """自定义部件，支持显示多个文本片段"""

    def __init__(self, text_items, main_layout=Qt.Vertical, parent=None):
        super().__init__(parent)

        # 创建主布局
        if main_layout == Qt.Vertical:
            self.main_layout = QVBoxLayout()
        else:
            self.main_layout = QHBoxLayout()

        self.main_layout.setContentsMargins(5, 5, 5, 5)
        self.main_layout.setSpacing(10)

        # 添加所有文本项
        for item_data in text_items:
            self.add_text_item(item_data)

        self.setLayout(self.main_layout)

    def add_text_item(self, item_data):
        """添加一个文本项到布局中"""
        # 确保color是QColor对象
        if not isinstance(item_data.color, QColor):
            item_data.color = QColor(0, 0, 0)

        # 根据文本方向选择标签类型
        if item_data.orientation == Qt.Vertical:
            label = RotatedLabel(item_data.text)
            label.setMinimumHeight(100)  # 垂直文本需要更多高度
        else:
            label = QLabel(item_data.text)

        # 设置字体大小
        font = QFont()
        font.setPointSize(item_data.font_size)
        label.setFont(font)

        # 设置文字颜色
        label.setStyleSheet(
            f"color: rgb({item_data.color.red()}, {item_data.color.green()}, {item_data.color.blue()});"
        )

        # 设置对齐方式
        label.setAlignment(item_data.h_align | item_data.v_align)

        self.main_layout.addWidget(label)


class CustomTableWidget(QTableWidget):
    """自定义表格控件"""

    def __init__(self, rows=0, cols=0, parent=None):
        super().__init__(rows, cols, parent)

    def set_text_cell(self, row, col, text_items, main_layout=Qt.Vertical):
        """在指定单元格设置多文本内容"""
        widget = StyledTextWidget(text_items, main_layout)
        self.setCellWidget(row, col, widget)


class ExampleWindow(QWidget):
    """示例窗口"""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('水平和垂直文本混合表格示例')
        self.setGeometry(100, 100, 1000, 500)

        # 创建一个3行5列的表格
        table = CustomTableWidget(3, 5, self)

        # 调整表格尺寸
        for col in range(5):
            table.setColumnWidth(col, 180)
        for row in range(3):
            table.setRowHeight(row, 150)  # 增加行高以容纳垂直文本

        # 第一行：水平文本
        row1_data = [
            [
                TextItemData(text="水平文本1", font_size=12),
                TextItemData(text="水平文本2", font_size=14, color=QColor(255, 0, 0))
            ],
            [
                TextItemData(text="左对齐", font_size=12, color=QColor(0, 0, 255), h_align=Qt.AlignLeft),
                TextItemData(text="右对齐", font_size=12, color=QColor(0, 128, 0), h_align=Qt.AlignRight)
            ],
            [
                TextItemData(text="小文本", font_size=10),
                TextItemData(text="大文本", font_size=16)
            ],
            [
                TextItemData(text="顶部对齐", font_size=12, v_align=Qt.AlignTop),
                TextItemData(text="底部对齐", font_size=12, v_align=Qt.AlignBottom)
            ],
            [
                TextItemData(text="水平混合1", font_size=12),
                TextItemData(text="水平混合2", font_size=14, color=QColor(128, 0, 128))
            ]
        ]

        # 第二行：垂直文本
        row2_data = [
            [
                TextItemData(text="垂直文本", font_size=12, orientation=Qt.Vertical),
            ],
            [
                TextItemData(text="红色垂直", font_size=14, color=QColor(255, 0, 0), orientation=Qt.Vertical),
                TextItemData(text="蓝色垂直", font_size=14, color=QColor(0, 0, 255), orientation=Qt.Vertical)
            ],
            [
                TextItemData(text="小垂直", font_size=10, orientation=Qt.Vertical),
                TextItemData(text="大垂直", font_size=16, orientation=Qt.Vertical)
            ],
            [
                TextItemData(text="垂直对齐1", font_size=12, orientation=Qt.Vertical),
                TextItemData(text="垂直对齐2", font_size=12, orientation=Qt.Vertical)
            ],
            [
                TextItemData(text="竖排文本", font_size=14, color=QColor(128, 0, 0), orientation=Qt.Vertical),
            ]
        ]

        # 第三行：混合文本
        row3_data = [
            [
                TextItemData(text="水平", font_size=14),
                TextItemData(text="垂直", font_size=14, color=QColor(255, 0, 0), orientation=Qt.Vertical)
            ],
            [
                TextItemData(text="左", font_size=12, h_align=Qt.AlignLeft),
                TextItemData(text="右竖", font_size=12, color=QColor(0, 128, 0),
                             orientation=Qt.Vertical, h_align=Qt.AlignRight)
            ],
            [
                TextItemData(text="小", font_size=10),
                TextItemData(text="大竖", font_size=16, orientation=Qt.Vertical)
            ],
            [
                TextItemData(text="上", font_size=12, v_align=Qt.AlignTop),
                TextItemData(text="下竖", font_size=12, orientation=Qt.Vertical, v_align=Qt.AlignBottom)
            ],
            [
                TextItemData(text="混合文本", font_size=14),
                TextItemData(text="竖排混合", font_size=12, color=QColor(128, 0, 128), orientation=Qt.Vertical),
                TextItemData(text="水平混合", font_size=10, color=QColor(0, 128, 128))
            ]
        ]

        # 填充表格数据
        for col, text_items in enumerate(row1_data):
            table.set_text_cell(0, col, text_items, Qt.Vertical)

        for col, text_items in enumerate(row2_data):
            table.set_text_cell(1, col, text_items, Qt.Horizontal)

        for col, text_items in enumerate(row3_data):
            table.set_text_cell(2, col, text_items, Qt.Horizontal)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ExampleWindow()
    window.show()
    sys.exit(app.exec_())
