class RotatedLabel(QLabel):
    """支持任意角度旋转的标签，修复坐标类型错误"""

    def __init__(self, text, parent=None, rotation=90):
        super().__init__(text, parent)
        self.rotation = rotation % 360  # 标准化角度（0-359度）
        self.setMinimumSize(30, 30)  # 最小尺寸确保可见

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.save()

        # 获取文本尺寸
        font_metrics = QFontMetrics(self.font())
        text_width = font_metrics.width(self.text())
        text_height = font_metrics.height()

        # 计算旋转中心（控件中心）
        center_x = self.width() / 2
        center_y = self.height() / 2

        # 根据不同角度进行特殊处理
        if self.rotation == 90:
            # 顺时针旋转90度
            painter.translate(center_x, center_y)
            painter.rotate(90)
            # 坐标转换为整数
            x = int(-center_y)
            y = int(center_x - text_height / 2)
            painter.drawText(x, y, self.text())

        elif self.rotation == 270 or self.rotation == -90:
            # 逆时针旋转90度（270度）
            painter.translate(center_x, center_y)
            painter.rotate(-90)
            # 坐标转换为整数
            x = int(center_y - text_width)
            y = int(-center_x + text_height / 2)
            painter.drawText(x, y, self.text())

        elif self.rotation == 180:
            # 旋转180度
            painter.translate(center_x, center_y)
            painter.rotate(180)
            # 坐标转换为整数
            x = int(-text_width / 2)
            y = int(text_height / 2)
            painter.drawText(x, y, self.text())

        else:
            # 其他角度通用处理
            painter.translate(center_x, center_y)
            painter.rotate(self.rotation)
            # 坐标转换为整数（关键修复）
            x = int(-text_width / 2)
            y = int(text_height / 2)
            painter.drawText(x, y, self.text())

        painter.restore()

    def sizeHint(self):
        """根据旋转角度返回合适的尺寸提示"""
        font_metrics = QFontMetrics(self.font())
        text_size = font_metrics.size(Qt.TextSingleLine, self.text())

        # 90度和270度旋转时交换宽高
        if self.rotation in (90, 270):
            return text_size.transposed()
        return text_size