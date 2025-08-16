import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt


class StyleTestWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("修复样式不生效问题")
        self.resize(400, 200)

        layout = QVBoxLayout(self)

        # 创建测试标签
        self.label_liunian_2 = QLabel("测试样式")
        layout.addWidget(self.label_liunian_2)

        # 调用样式设置方法
        self.set_label_style(
            self.label_liunian_2,
            bg_color=(255, 0, 0),  # 红色背景
            text_color=(0, 255, 0),  # 绿色字体
            font_size=20
        )

    def set_label_style(self, label, bg_color, text_color, font_size):
        # 1. 先单独测试文本居中（确认基础功能正常）
        label.setAlignment(Qt.AlignCenter)

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

        # 3. 打印样式表（用于调试，确认格式正确）
        print("应用的样式表：")
        print(style_sheet)

        # 4. 强制清除现有样式并应用新样式
        label.setStyleSheet("")  # 先清除旧样式
        label.setStyleSheet(style_sheet)

        # 5. 确保没有其他属性干扰
        # label.setFlat(False)  # 禁用flat属性（可能影响背景显示）
        label.setAttribute(Qt.WA_StyledBackground, True)  # 强制启用样式背景


if __name__ == "__main__":
    app = QApplication(sys.argv)
    # 检查是否有全局样式表干扰
    if app.styleSheet():
        print("警告：存在全局样式表，可能导致样式冲突！")
        # 临时清除全局样式表（仅测试用）
        app.setStyleSheet("")

    window = StyleTestWindow()
    window.show()
    sys.exit(app.exec_())
