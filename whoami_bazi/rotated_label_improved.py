import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPainter, QFont, QFontMetrics


class VerticalTextLabel(QLabel):
    """可调整字符间距的竖直显示标签"""

    def __init__(self, text, spacing=10, parent=None):  # 新增spacing参数控制间距
        super().__init__("", parent)
        self._text = text
        self._spacing = spacing  # 字符之间的额外间距
        self.setMinimumSize(60, 150)

        # 配置字体
        font = QFont()
        font.setPointSize(24)
        font.setBold(True)
        self.setFont(font)

    # 新增设置间距的方法，方便动态调整
    def set_spacing(self, spacing):
        self._spacing = spacing
        self.update()  # 触发重绘

    def paintEvent(self, event):
        if not self.isVisible():
            return

        painter = QPainter(self)
        painter.eraseRect(self.rect())
        painter.setRenderHint(QPainter.TextAntialiasing)

        font = self.font()
        painter.setFont(font)
        painter.setPen(self.palette().color(self.foregroundRole()))

        font_metrics = QFontMetrics(font)
        char_height = font_metrics.height()
        char_width = max(font_metrics.width(c) for c in self._text)

        start_x = (self.width() - char_width) // 2
        start_y = font_metrics.ascent() + 10

        # 核心修改：在字符高度基础上增加额外间距
        for i, char in enumerate(self._text):
            # 字符间距 = 字符高度 + 自定义间距
            y_pos = start_y + i * (char_height + self._spacing)
            if y_pos < self.height() - 10:
                painter.drawText(start_x, y_pos, char)

    def sizeHint(self):
        font_metrics = QFontMetrics(self.font())
        char_height = font_metrics.height()
        width = max(font_metrics.width(c) for c in self._text) + 20
        # 高度计算也要包含额外间距
        height = len(self._text) * char_height + (len(self._text) - 1) * self._spacing + 30
        return QSize(width, height)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("带间距的竖直显示'癸未'")
    window.setMinimumSize(120, 250)  # 适当增大窗口高度

    layout = QVBoxLayout(window)
    layout.setContentsMargins(30, 30, 30, 30)

    # 创建标签时指定间距（这里设为20，数值越大间距越宽）
    vertical_label = VerticalTextLabel("癸未", spacing=20)
    vertical_label.setStyleSheet("color: #333333; background: #f0f0f0;")

    # 也可以动态调整间距：vertical_label.set_spacing(30)

    layout.addWidget(vertical_label)

    window.show()
    sys.exit(app.exec_())
