import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from database import DatabaseManager
from models import ProfileMatchingModel
from views.input_view import InputView
from views.output_view import OutputView
from views.about_view import AboutView

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Seleksi Asisten Laboratorium")
        self.setGeometry(100, 100, 1000, 600)
        self.db_manager = DatabaseManager()
        self.model = ProfileMatchingModel()
        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("QMainWindow { background-color: #f5f5f5; }")
        self.init_menu_bar()
        self.init_status_bar()
        self.init_hamburger_menu()

    def init_menu_bar(self):
        menubar = self.menuBar()
        help_menu = menubar.addMenu("Help")

        about_action = QAction("Tentang", self)
        about_action.setShortcut("Ctrl+I")
        about_action.triggered.connect(self.show_about_view)
        help_menu.addAction(about_action)

        exit_action = QAction("Keluar", self)
        exit_action.setShortcut("Ctrl+Q")
        exit_action.triggered.connect(self.close)
        help_menu.addAction(exit_action)

    def show_about_view(self):
        self.show_view(2)

    def init_status_bar(self):
        statusbar = QStatusBar()
        statusbar.showMessage("Muhammad Fajar Maulana - F1D022072")
        statusbar.setStyleSheet("QStatusBar { background-color: #e0e0e0; color: #333; padding: 5px; }")
        self.setStatusBar(statusbar)

    def init_hamburger_menu(self):
        main_widget = QWidget()
        main_layout = QHBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.sidebar = QFrame()
        self.sidebar.setFixedWidth(200)
        self.sidebar.setObjectName("sidebar")
        self.sidebar.setStyleSheet("QFrame#sidebar { background-color: #2c3e50; border-right: 1px solid #1a252f; }")

        sidebar_layout = QVBoxLayout(self.sidebar)
        sidebar_layout.setContentsMargins(0, 20, 4, 0)
        sidebar_layout.setSpacing(10)

        self.hamburger_button = QPushButton("☰")
        self.hamburger_button.setFixedSize(40, 40)
        self.hamburger_button.setObjectName("hamburgerButton")
        self.hamburger_button.clicked.connect(self.toggle_sidebar)
        self.hamburger_button.setStyleSheet(
            "QPushButton#hamburgerButton { background-color: #34495e; color: white; border: none; font-size: 20px; "
            "border-radius: 5px; margin-left: 17px; padding: 5px; min-width: 30px; min-height: 30px; } "
            "QPushButton#hamburgerButton:hover { background-color: #3d566e; }"
        )

        self.input_button = self.create_menu_button("Input Data", "input.png")
        self.output_button = self.create_menu_button("Perhitungan", "calculate.png")
        self.about_button = self.create_menu_button("Tentang", "about.png")

        sidebar_layout.addWidget(self.hamburger_button, 0, Qt.AlignLeft)
        sidebar_layout.addWidget(self.input_button)
        sidebar_layout.addWidget(self.output_button)
        sidebar_layout.addWidget(self.about_button)
        sidebar_layout.addStretch()

        self.stacked_widget = QWidget()
        self.stacked_layout = QVBoxLayout(self.stacked_widget)
        self.stacked_layout.setContentsMargins(20, 20, 20, 20)

        self.input_view = InputView(self.db_manager)
        self.output_view = OutputView(self.db_manager, self.model)
        self.about_view = AboutView()

        self.stacked_layout.addWidget(self.input_view)
        self.stacked_layout.addWidget(self.output_view)
        self.stacked_layout.addWidget(self.about_view)

        for i in range(self.stacked_layout.count()):
            self.stacked_layout.itemAt(i).widget().hide()
        self.stacked_layout.itemAt(0).widget().show()

        self.input_button.setChecked(True)

        self.input_button.clicked.connect(lambda: self.show_view(0))
        self.output_button.clicked.connect(lambda: self.show_view(1))
        self.about_button.clicked.connect(lambda: self.show_view(2))

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stacked_widget)
        self.setCentralWidget(main_widget)

        self.sidebar_animation = QPropertyAnimation(self.sidebar, b"minimumWidth")
        self.sidebar_animation.setDuration(300)
        self.sidebar_animation.setEasingCurve(QEasingCurve.InOutQuad)
        self.sidebar_expanded = True

    def create_menu_button(self, text, icon_name):
        button = QPushButton(text)
        button.setFixedHeight(50)
        button.setObjectName("menuButton")

        icon_path = os.path.join("assets", "icon", icon_name)
        if os.path.exists(icon_path):
            button.setIcon(QIcon(icon_path))
            button.setIconSize(QSize(24, 24))

        button.setStyleSheet(
            "QPushButton#menuButton { background-color: transparent; color: white; text-align: left; padding-left: 15px; "
            "font-size: 14px; border: none; border-radius: 5px; margin: 5px 10px; } "
            "QPushButton#menuButton:hover { background-color: #34495e; padding-left: 20px; border-left: 3px solid #3498db; } "
            "QPushButton#menuButton:pressed { background-color: #2980b9; } "
            "QPushButton#menuButton:checked { background-color: #34495e; padding-left: 20px; "
            "border-left: 3px solid #3498db; font-weight: bold; }"
        )

        button.setCheckable(True)
        return button

    def toggle_sidebar(self):
        start_width = 200 if self.sidebar_expanded else 50
        end_width = 50 if self.sidebar_expanded else 200

        self.sidebar_animation.setStartValue(start_width)
        self.sidebar_animation.setEndValue(end_width)
        self.sidebar_animation.start()

        if not self.sidebar_expanded:
            self.input_button.setText("Input Data")
            self.output_button.setText("Perhitungan")
            self.about_button.setText("Tentang")
        else:
            self.input_button.setText("")
            self.output_button.setText("")
            self.about_button.setText("")

        self.sidebar_expanded = not self.sidebar_expanded

    def show_view(self, index):
        self.input_button.setChecked(index == 0)
        self.output_button.setChecked(index == 1)
        self.about_button.setChecked(index == 2)

        for i in range(self.stacked_layout.count()):
            widget = self.stacked_layout.itemAt(i).widget()
            widget.setVisible(i == index)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
