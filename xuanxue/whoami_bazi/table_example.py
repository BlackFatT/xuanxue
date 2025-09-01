import sys
from PyQt5.QtWidgets import (QApplication, QTableWidget, QTableWidgetItem,
                             QWidget, QVBoxLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont


class StyledTable(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 设置窗口基本属性
        self.setWindowTitle('表格单元格样式自定义')
        self.setGeometry(100, 100, 800, 150)

        # 创建表格，1行5列
        table = QTableWidget(1, 5, self)

        # 设置列宽，使内容更好地展示
        for col in range(5):
            table.setColumnWidth(col, 150)

        # 定义每列的样式参数：(文本, 字体大小, 颜色, 水平对齐, 垂直对齐)
        column_styles = [
            ("左对齐顶部", 12, QColor(0, 0, 0), Qt.AlignLeft, Qt.AlignTop),
            ("居中对齐", 14, QColor(255, 0, 0), Qt.AlignCenter, Qt.AlignVCenter),
            ("右对齐底部", 16, QColor(0, 128, 0), Qt.AlignRight, Qt.AlignBottom),
            ("两端对齐居中", 10, QColor(0, 0, 255), Qt.AlignJustify, Qt.AlignVCenter),
            ("居中对齐顶部", 18, QColor(128, 0, 128), Qt.AlignCenter, Qt.AlignTop)
        ]

        # 为每个单元格应用样式
        for col, (text, font_size, color, h_align, v_align) in enumerate(column_styles):
            # 创建表格项
            item = QTableWidgetItem(text)

            # 设置字体大小
            font = QFont()
            font.setPointSize(font_size)
            item.setFont(font)

            # 设置文字颜色
            item.setForeground(color)

            # 设置对齐方式（水平和垂直组合）
            item.setTextAlignment(h_align | v_align)

            # 将项添加到表格
            table.setItem(0, col, item)

        # 设置布局
        layout = QVBoxLayout()
        layout.addWidget(table)
        self.setLayout(layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StyledTable()
    window.show()
    sys.exit(app.exec_())
