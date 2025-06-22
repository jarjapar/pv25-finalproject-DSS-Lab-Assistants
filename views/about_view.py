from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
    QTabWidget, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt

class AboutView(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        main_layout = QVBoxLayout()
        
        # Profile section
        profile_layout = QVBoxLayout()
        profile_layout.addWidget(QLabel("Profil Pengembang"))
        profile_layout.addWidget(QLabel("Nama: Muhammad Fajar Maulana"))
        profile_layout.addWidget(QLabel("NIM: F1D022072"))
        
        # Tab widget for about information
        tab_widget = QTabWidget()
        
        # Kriteria tab
        criteria_tab = QWidget()
        criteria_layout = QVBoxLayout()
        
        criteria_table = QTableWidget()
        criteria_table.setRowCount(5)
        criteria_table.setColumnCount(3)
        criteria_table.setHorizontalHeaderLabels(["Kriteria", "Bobot", "Target"])
        
        criteria_data = [
            ("IPK", "25%", "4"),
            ("Penguasaan Jaringan Komputer", "20%", "4"),
            ("Penguasaan Bahasa Pemrograman", "20%", "5"),
            ("Komunikasi dan Kerjasama Tim", "20%", "4"),
            ("Kedisiplinan dan Tanggung Jawab", "15%", "4")
        ]
        
        for row, (criterion, weight, target) in enumerate(criteria_data):
            criteria_table.setItem(row, 0, QTableWidgetItem(criterion))
            criteria_table.setItem(row, 1, QTableWidgetItem(weight))
            criteria_table.setItem(row, 2, QTableWidgetItem(target))
        
        criteria_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        criteria_layout.addWidget(criteria_table)
        criteria_tab.setLayout(criteria_layout)
        
        # IPK Scale tab
        ipk_tab = QWidget()
        ipk_layout = QVBoxLayout()
        
        ipk_table = QTableWidget()
        ipk_table.setRowCount(5)
        ipk_table.setColumnCount(2)
        ipk_table.setHorizontalHeaderLabels(["Rentang IPK", "Nilai"])
        
        ipk_data = [
            ("3.80 - 4.00", "5"),
            ("3.20 - 3.79", "4"),
            ("2.80 - 3.19", "3"),
            ("2.00 - 2.79", "2"),
            ("0.00 - 1.99", "1")
        ]
        
        for row, (range_, value) in enumerate(ipk_data):
            ipk_table.setItem(row, 0, QTableWidgetItem(range_))
            ipk_table.setItem(row, 1, QTableWidgetItem(value))
        
        ipk_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        ipk_layout.addWidget(ipk_table)
        ipk_tab.setLayout(ipk_layout)
        
        # GAP Values tab
        gap_tab = QWidget()
        gap_layout = QVBoxLayout()
        
        gap_table = QTableWidget()
        gap_table.setRowCount(11)
        gap_table.setColumnCount(3)
        gap_table.setHorizontalHeaderLabels(["GAP", "Nilai", "Keterangan"])
        
        gap_data = [
            ("0", "6", "Tidak ada GAP (Kompetensi sesuai)"),
            ("1", "5.5", "Kelebihan 1 tingkat"),
            ("-1", "5", "Kekurangan 1 tingkat"),
            ("2", "4.5", "Kelebihan 2 tingkat"),
            ("-2", "4", "Kekurangan 2 tingkat"),
            ("3", "3.5", "Kelebihan 3 tingkat"),
            ("-3", "3", "Kekurangan 3 tingkat"),
            ("4", "2.5", "Kelebihan 4 tingkat"),
            ("-4", "2", "Kekurangan 4 tingkat"),
            ("5", "1.5", "Kelebihan 5 tingkat"),
            ("-5", "1", "Kekurangan 5 tingkat")
        ]
        
        for row, (gap, value, desc) in enumerate(gap_data):
            gap_table.setItem(row, 0, QTableWidgetItem(gap))
            gap_table.setItem(row, 1, QTableWidgetItem(value))
            gap_table.setItem(row, 2, QTableWidgetItem(desc))
        
        gap_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        gap_layout.addWidget(gap_table)
        gap_tab.setLayout(gap_layout)
        
        # Add tabs
        tab_widget.addTab(criteria_tab, "Kriteria")
        tab_widget.addTab(ipk_tab, "Skala IPK")
        tab_widget.addTab(gap_tab, "Nilai GAP")
        
        # Add widgets to main layout
        main_layout.addLayout(profile_layout)
        main_layout.addWidget(QLabel("Tentang Aplikasi:"))
        main_layout.addWidget(tab_widget)
        
        self.setLayout(main_layout)