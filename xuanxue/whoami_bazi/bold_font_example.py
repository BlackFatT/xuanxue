import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


class BoldFontExample(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("增强字体加粗效果")
        self.resize(400, 300)

        layout = QVBoxLayout(self)
        layout.setSpacing(20)

        # 1. 普通加粗（可能不够明显）
        label1 = QLabel("普通加粗：setBold(True)")
        font1 = QFont()
        font1.setFamily("SimHei")  # 使用支持粗体的字体
        font1.setPointSize(14)
        font1.setBold(True)  # 基础加粗
        label1.setFont(font1)
        layout.addWidget(label1)

        # 2. 更高字重的字体（推荐）
        label2 = QLabel("高字重字体：Arial Black")
        font2 = QFont()
        font2.setFamily("Arial Black")  # 本身就是粗体设计的字体
        font2.setPointSize(14)
        label2.setFont(font2)
        layout.addWidget(label2)

        # 3. 样式表设置粗体（支持900最高字重）
        label3 = QLabel("样式表：font-weight: 900")
        label3.setStyleSheet("""
            font-family: SimHei;
            font-size: 14pt;
            font-weight: 900;  /* 900是CSS最高字重，比bold更粗 */
        """)
        layout.addWidget(label3)

        # 4. 叠加效果（不推荐，但极端情况可用）
        label4 = QLabel("叠加效果（不推荐）")
        font4 = QFont()
        font4.setFamily("SimHei")
        font4.setPointSize(14)
        font4.setBold(True)
        label4.setFont(font4)
        # 叠加样式表加粗（可能在部分字体上有效）
        label4.setStyleSheet("font-weight: 900;")
        layout.addWidget(label4)

        # 居中显示
        for label in [label1, label2, label3, label4]:
            label.setAlignment(Qt.AlignCenter)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = BoldFontExample()
    window.show()
    sys.exit(app.exec_())
