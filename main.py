#main file of Network Scanner
import sys
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Scanner')
        self.resize(1200,800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        #Header
        self.header = QLabel("  MAIN MENU")
        self.header.setAlignment(Qt.AlignLeft)
        self.header.setStyleSheet("background-color: #3b4cc0; color: black; font-size: 32px;")
        self.header.setFixedHeight(60)

        #Lišta s možnostmi
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout()
        self.sidebar.setLayout(sidebar_layout)
        self.sidebar.setFixedWidth(150)
        self.sidebar.setStyleSheet("background-color: #4cc0e0;")
        sidebar_layout.setSpacing(0)
        sidebar_layout.setAlignment(Qt.AlignTop)
        
        #Možnosti v liště
        btn0 = QPushButton("Port Scan")
        btn0.setStyleSheet("""
            QPushButton {
                background-color: #0077aa;
                color: black;
                font-size: 20px;
                border-radius: 8px;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #0099cc;
            }
            """)
        btn1 = QPushButton("IP Scan")
        btn1.setStyleSheet("""
            QPushButton{
                background-color:#0077aa;
                color: black;
                font-size: 20px;
                border-radius: 8px;
                padding: 10px;
            }        
            QPushButton:hover{
                background-color: #0099cc;
            }
            """)
        
        sidebar_layout.addWidget(btn0)
        sidebar_layout.addWidget(btn1)
        
        # Sekce pro data
        self.data_area = QWidget()
        self.data_area.setStyleSheet("background-color: #a0e0f0;")
        self.data_layout = QVBoxLayout()
        self.data_area.setLayout(self.data_layout)
        data_label = QLabel("Work in Progress")
        data_label.setAlignment(Qt.AlignCenter)
        data_label.setStyleSheet('color: black;font-size: 60px')
        self.data_layout.addWidget(data_label)

        # Rozložení hlavního obsahu
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.sidebar, 1)
        content_layout.addWidget(self.data_area, 3)

        # Celkové rozložení
        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addLayout(content_layout)
        main_widget.setLayout(layout)
        
# Run the application

app = QApplication(sys.argv)
display = Window()
display.show()
sys.exit(app.exec_())
