from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QFont, QFontMetrics, QColor


# class VerticalTextLabel(QLabel):
#     """可调整字符间距的竖直显示标签"""
#
#     def __init__(self, text, spacing=10, parent=None):  # 新增spacing参数控制间距
#         super().__init__("", parent)
#         self._text = text
#         self._spacing = spacing  # 字符之间的额外间距
#         # self.setMinimumSize(60, 150)
#         self.setMinimumSize(60, 90)
#
#         # 配置字体
#         font = QFont()
#         # font.setPointSize(24)
#         font.setPointSize(18)
#         font.setBold(True)
#         self.setFont(font)
#
#     # 新增设置间距的方法，方便动态调整
#     def set_spacing(self, spacing):
#         self._spacing = spacing
#         self.update()  # 触发重绘
#
#     def paintEvent(self, event):
#         if not self.isVisible():
#             return
#
#         painter = QPainter(self)
#         painter.eraseRect(self.rect())
#         painter.setRenderHint(QPainter.TextAntialiasing)
#
#         font = self.font()
#         painter.setFont(font)
#         painter.setPen(self.palette().color(self.foregroundRole()))
#
#         font_metrics = QFontMetrics(font)
#         char_height = font_metrics.height()
#         char_width = max(font_metrics.width(c) for c in self._text)
#
#         start_x = (self.width() - char_width) // 2
#         start_y = font_metrics.ascent() + 10
#
#         # 核心修改：在字符高度基础上增加额外间距
#         for i, char in enumerate(self._text):
#             # 字符间距 = 字符高度 + 自定义间距
#             y_pos = start_y + i * (char_height + self._spacing)
#             if y_pos < self.height() - 10:
#                 painter.drawText(start_x, y_pos, char)
#
#     def sizeHint(self):
#         font_metrics = QFontMetrics(self.font())
#         char_height = font_metrics.height()
#         width = max(font_metrics.width(c) for c in self._text) + 20
#         # 高度计算也要包含额外间距
#         height = len(self._text) * char_height + (len(self._text) - 1) * self._spacing + 30
#         return QSize(width, height)


class VerticalTextLabel(QLabel):
    """可调整字符间距且文字垂直居中的竖直显示标签"""

    def __init__(self, text, color="#333333", fontsize=18, spacing=10, parent=None):
        super().__init__("", parent)
        self._text = text
        self._spacing = spacing
        self._color = color
        self.setMinimumSize(60, 90)

        # 配置字体
        font = QFont()
        font.setPointSize(fontsize)
        font.setBold(True)
        self.setFont(font)

        self.apply_color()

    def set_spacing(self, spacing):
        self._spacing = spacing
        self.update()

    def paintEvent(self, event):
        if not self.isVisible():
            return

        painter = QPainter(self)
        painter.eraseRect(self.rect())
        painter.setRenderHint(QPainter.TextAntialiasing)

        font = self.font()
        painter.setFont(font)
        painter.setPen(self.palette().color(self.foregroundRole()))
        # painter.setPen(self.palette().color(self._color))

        font_metrics = QFontMetrics(font)
        char_height = font_metrics.height()
        char_width = max(font_metrics.width(c) for c in self._text)
        text_count = len(self._text)

        # 计算所有文字的总高度（包括间距）
        total_text_height = text_count * char_height + (text_count - 1) * self._spacing

        # 计算竖直方向居中的起始Y坐标
        # 控件可用高度 = 控件高度 - 上下边距(20)
        # 居中起始位置 = 控件顶部边距 + (可用高度 - 总文字高度) / 2
        top_margin = 10
        available_height = self.height() - 20  # 减去上下边距
        start_y = top_margin + (available_height - total_text_height) // 2 + font_metrics.ascent()

        # 水平居中起始X坐标
        start_x = (self.width() - char_width) // 2

        # 绘制字符
        for i, char in enumerate(self._text):
            y_pos = start_y + i * (char_height + self._spacing)
            if y_pos < self.height() - 10:
                painter.drawText(start_x, y_pos, char)

    def apply_color(self):
        """应用字体颜色"""
        self.setStyleSheet(f"color: {self._color};")

    def sizeHint(self):
        font_metrics = QFontMetrics(self.font())
        char_height = font_metrics.height()
        width = max(font_metrics.width(c) for c in self._text) + 20
        height = len(self._text) * char_height + (len(self._text) - 1) * self._spacing + 30
        return QSize(width, height)

# # 使用示例
# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#
#     window = QWidget()
#     window.setWindowTitle("汉字竖直显示（修复版）")
#     layout = QVBoxLayout(window)
#     layout.setContentsMargins(20, 20, 20, 20)
#
#     # 横向显示
#     horizontal_label = QLabel("横向：癸未")
#     layout.addWidget(horizontal_label)
#
#     # 竖直显示
#     vertical_label = VerticalTextLabel("癸未")
#     # 设置字体样式
#     font = QFont()
#     font.setPointSize(16)
#     font.setBold(True)
#     vertical_label.setFont(font)
#     # 设置文字颜色
#     vertical_label.setStyleSheet("color: #8B0000;")  # 深红色
#     layout.addWidget(vertical_label)
#
#     # 更多示例
#     layout.addWidget(QLabel("横向：甲乙丙丁"))
#     layout.addWidget(VerticalTextLabel("甲乙丙丁"))
#
#     window.setLayout(layout)
#     window.resize(200, 300)
#     window.show()
#     sys.exit(app.exec_())
