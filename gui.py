import network_scan, this_pc
import threading
import sys
import ipaddress
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit


def start_app():
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec())


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Scanner')
        self.resize(1200, 800)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Header
        self.header = QLabel("  MAIN MENU")
        self.header.setAlignment(Qt.AlignLeft)
        self.header.setStyleSheet("background-color: #3b4cc0; color: black; font-size: 32px;")
        self.header.setFixedHeight(60)

        # Sidebar
        self.sidebar = QWidget()
        sidebar_layout = QVBoxLayout(self.sidebar)
        self.sidebar.setFixedWidth(180)
        self.sidebar.setStyleSheet("background-color: #4cc0e0;")
        sidebar_layout.setSpacing(0)
        sidebar_layout.setAlignment(Qt.AlignTop)

        btn0 = QPushButton("Toto PC")
        btn0.setStyleSheet(
                    """QPushButton 
                    {
                    background-color: #0077aa;
                    color: black;
                    font-size: 20px;
                    border-radius: 8px;
                    padding: 10px;
                    }
                    QPushButton:hover 
                    {
                    background-color: #0099cc;
                    }""")
        btn1 = QPushButton("Network Scan")
        btn1.setStyleSheet(
                            """QPushButton 
                            {
                            background-color: #0077aa;
                            color: black;
                            font-size: 20px;
                            border-radius: 8px;
                            padding: 10px;
                            }
                            QPushButton:hover 
                            {
                            background-color: #0099cc;
                            }""")
        btn2 = QPushButton("IP Scan")
        btn2.setStyleSheet(
                    """QPushButton 
                    {
                    background-color: #0077aa;
                    color: black;
                    font-size: 20px;
                    border-radius: 8px;
                    padding: 10px;
                    }
                    QPushButton:hover 
                    {
                    background-color: #0099cc;
                    }""")

        sidebar_layout.addWidget(btn0)
        sidebar_layout.addWidget(btn1)
        sidebar_layout.addWidget(btn2)

        btn0.clocked.connect(self.show_this_pc)
        btn1.clicked.connect(self.show_port_scan_page)
        btn2.clicked.connect(self.show_network_scan_page)

        # Data area
        self.data_area = QWidget()
        self.data_area.setStyleSheet("background-color: #a0e0f0;")
        self.data_layout = QVBoxLayout(self.data_area)

        data_label = QLabel("Work in Progress")
        data_label.setAlignment(Qt.AlignCenter)
        data_label.setStyleSheet('color: black;font-size: 60px')
        self.data_layout.addWidget(data_label)

        # Main layout
        content_layout = QHBoxLayout()
        content_layout.addWidget(self.sidebar, 1)
        content_layout.addWidget(self.data_area, 3)

        layout = QVBoxLayout()
        layout.addWidget(self.header)
        layout.addLayout(content_layout)
        main_widget.setLayout(layout)

    def clear_data_area(self):
        while self.data_layout.count():
            item = self.data_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def load_page(self, widget):
        self.clear_data_area()
        self.data_layout.addWidget(widget)
    
    def show_this_pc(self):
        pocitac = this_pc.PC()
        pocitac.collect()

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.setSpacing(0)
        layout.setContentsMargins(10,0,0,40)

        title = QLabel("Informace o tomto PC")
        title.setStyleSheet("font-size: 40px; color: black; margin: 0px; padding: 0px")
        title.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        title.setFixedHeight(50)

        ip_site = ipaddress.IPv4Network(f"{pocitac.ipv4}/{pocitac.subnet_mask}", strict=False)

        form_widget = QWidget()
        form = QFormLayout(form_widget)
        form.setSpacing(0)
        form.setContentsMargins(20,30,0,0)
        form_widget.setStyleSheet(
                """
                QLabel {
                font-size: 20px;
                color: black;
                }""")

        form.addRow("IPv4 adresa sítě: ", QLabel(str(ip_site)))
        form.addRow("Maska sítě: ", QLabel(pocitac.subnet_mask))
        form.addRow("IPv4 adresa zařízení: ", QLabel(pocitac.ipv4))
        form.addRow("IPv6 adresa zařízení: ",QLabel(pocitac.ipv6))
        form.addRow("IPv4 adresa gateway: ", QLabel(pocitac.gateway_ip))
        form.addRow("DNS servery:",None)
        for i in pocitac.dns_servery:
            ip, jmeno = i
            if "NetBIOS" in jmeno or ip is None:
                continue
            form.addRow(QLabel(""),QLabel(f"{ip}"))

        layout.addWidget(title)
        layout.addWidget(form_widget)
        self.load_page(page)

    def show_port_scan_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Port Scan")
        title.setStyleSheet("font-size: 40px; color: black;")
        title.setAlignment(Qt.AlignCenter)

        input_ip = QLineEdit()
        input_ip.setPlaceholderText("Zadej IP adresu")
        input_ip.setStyleSheet("font-size: 20px; color: black")

        btn = QPushButton("Scan ports")
        btn.clicked.connect(lambda: self.run_port_scan(input_ip.text())) #Dopiš funkci

        self.label = QLabel("")
        self.label.setStyleSheet("font-size: 20px; color: black")

        layout.addWidget(title)
        layout.addWidget(input_ip)
        layout.addWidget(btn)
        layout.addWidget(self.label)

        self.load_page(page)

    def show_network_scan_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        rowIPStart = QHBoxLayout()
        rowIPRozsah = QHBoxLayout()

        title = QLabel("Network Scan")
        title.setStyleSheet("font-size: 40px; color: black;")
        title.setAlignment(Qt.AlignCenter)

        input_ip = QLineEdit()
        input_ip.setPlaceholderText("Např. 192.168.0.")
        input_ip.setStyleSheet("font-size: 20px; color: black")

        ip_start = QLineEdit()
        ip_start.setPlaceholderText("0-255")
        ip_start.setStyleSheet("font-size: 20px; color: black")

        ip_konec = QLineEdit()
        ip_konec.setPlaceholderText("0-255")
        ip_konec.setStyleSheet("font-size:20px; color: black")

        btn = QPushButton("Scan network")
        btn.setStyleSheet(
            """QPushButton{
            background-color: white;
            color: black;
            font-size: 20px;
            border-radius: 8px;
            padding: 10px;
            }""")
        btn.clicked.connect(lambda: self.scan_click(input_ip,ip_start,ip_konec))
        
        self.label = QLabel("")
        self.label.setStyleSheet("font-size: 20px; color: black")


#Vykreslení layoutu stránky
        layout.addWidget(title)

        rowIPStart = QHBoxLayout()
        rowIPtext = QLabel("Zadej základ IP: ")
        rowIPtext.setStyleSheet("font-size: 20px; color: black;")
        rowIPStart.addWidget(rowIPtext)
        rowIPStart.addWidget(input_ip)
        layout.addLayout(rowIPStart)

        rowIPMinText = QLabel("Zadej rozsah: ")
        rowIPMinText.setStyleSheet("font-size: 20px; color: black;")
        rowIPRozsah.addWidget(rowIPMinText)
        rowIPRozsah.addWidget(ip_start)
        rowIPRozsah.addWidget(ip_konec)

        layout.addLayout(rowIPRozsah)
        layout.addWidget(btn)
        layout.addWidget(self.label)

        aktiv_text = QLabel("Využívané IP adresy:")
        aktiv_text.setStyleSheet("font-size: 20px; color: black")
        layout.addWidget(aktiv_text)

        self.aktivni_ip = QTextEdit()
        self.aktivni_ip.setReadOnly(True)
        self.aktivni_ip.setStyleSheet("""
                     QTextEdit {
                   background-color: #1e1e1e;
                   color: #00ff00;
                   font-size: 18px;
                   border: 2px solid #0099cc;
                   padding: 10px;
               }""")
               
        layout.addWidget(self.aktivni_ip)
        self.load_page(page)
       
       
    def scan_click(self, input_ip, ip_start, ip_konec):
        self.aktivni_ip.setText("Vyhledávání")
       
        self.scan_result = None
       
        def worker():
            self.scan_result = network_scan.run_network_scan(input_ip.text(),int(ip_start.text()),int(ip_konec.text()))
       
        thread = threading.Thread(target=worker, daemon=True)
        thread.start()
       
        # timer který kontroluje, zda vlákno skončilo
        def check_finished():
            if self.scan_result is not None:
                text = ""
                for ip, hostname in self.scan_result:
                    if hostname:
                        text += f"{ip} — {hostname}\n"
                    else:
                        text += f"{ip} — Neznámý host\n"
               
                self.aktivni_ip.setText(text)
                timer.stop()
       
        timer = QTimer()
        timer.timeout.connect(check_finished)
        timer.start(100)  # kontrola každých 100 ms   
