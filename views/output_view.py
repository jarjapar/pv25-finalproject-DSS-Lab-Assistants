# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'output_view.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

import csv
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets

class OutputView(QWidget):
    def __init__(self, db_manager, model):
        super().__init__()
        self.db_manager = db_manager
        self.model = model
        self.setupUi()

    def setupUi(self):
        self.setObjectName("OutputView")
        self.resize(1000, 600)

        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")

        self.labelInput = QtWidgets.QLabel(self)
        self.labelInput.setObjectName("labelInput")
        self.verticalLayout.addWidget(self.labelInput)

        self.input_table = QtWidgets.QTableWidget(self)
        self.input_table.setObjectName("input_table")
        self.input_table.setColumnCount(6)
        self.input_table.setRowCount(0)
        self.input_table.setHorizontalHeaderLabels([
            "Nama", "IPK", "Jaringan", "Pemrograman", 
            "Komunikasi", "Disiplin"
        ])
        self.input_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.input_table)

        self.buttonLayout = QtWidgets.QHBoxLayout()
        self.buttonLayout.setObjectName("buttonLayout")

        self.calculate_button = QtWidgets.QPushButton(self)
        self.calculate_button.setObjectName("calculate_button")
        self.calculate_button.setStyleSheet(
            "QPushButton { background-color: #2196F3; color: white; padding: 8px 16px; "
            "border: none; border-radius: 4px; font-weight: bold; } "
            "QPushButton:hover { background-color: #0b7dda; }"
        )
        self.buttonLayout.addWidget(self.calculate_button)

        self.export_button = QtWidgets.QPushButton(self)
        self.export_button.setObjectName("export_button")
        self.export_button.setEnabled(False)
        self.export_button.setStyleSheet(
            "QPushButton { background-color: #ff9800; color: white; padding: 8px 16px; "
            "border: none; border-radius: 4px; font-weight: bold; } "
            "QPushButton:hover { background-color: #e68a00; }"
        )
        self.buttonLayout.addWidget(self.export_button)

        self.verticalLayout.addLayout(self.buttonLayout)

        self.labelResult = QtWidgets.QLabel(self)
        self.labelResult.setObjectName("labelResult")
        self.verticalLayout.addWidget(self.labelResult)

        self.result_table = QtWidgets.QTableWidget(self)
        self.result_table.setObjectName("result_table")
        self.result_table.setColumnCount(8)
        self.result_table.setRowCount(0)
        self.result_table.setHorizontalHeaderLabels([
            "Nama", "IPK", "Jaringan", "Pemrograman", 
            "Komunikasi", "Disiplin", "Nilai Akhir", "Ranking"
        ])
        self.result_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.verticalLayout.addWidget(self.result_table)

        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)

        self.calculate_button.clicked.connect(self.calculate_results)
        self.export_button.clicked.connect(self.export_to_csv)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.labelInput.setText(_translate("OutputView", "Data Hasil Input:"))
        self.labelResult.setText(_translate("OutputView", "Hasil Perhitungan:"))
        self.calculate_button.setText(_translate("OutputView", "Hitung Profile Matching"))
        self.export_button.setText(_translate("OutputView", "Export ke CSV"))

    def showEvent(self, event):
        self.load_input_data()
        super().showEvent(event)

    def load_input_data(self):
        candidates = self.db_manager.get_all_candidates()
        self.input_table.setRowCount(0)
        self.input_table.setRowCount(len(candidates))

        for row, candidate in enumerate(candidates):
            for col, value in enumerate(candidate[1:]):  # Skip ID
                item = QtWidgets.QTableWidgetItem(str(value))
                item.setFlags(item.flags() ^ QtCore.Qt.ItemIsEditable)
                self.input_table.setItem(row, col, item)

    def calculate_results(self):
        candidates = self.db_manager.get_all_candidates()
        if not candidates:
            QtWidgets.QMessageBox.warning(self, "Peringatan", "Tidak ada data kandidat untuk dihitung.")
            return

        ranked_candidates = self.model.rank_candidates(candidates)
        self.db_manager.save_results(ranked_candidates)
        self.show_results(ranked_candidates)
        self.export_button.setEnabled(True)

    def show_results(self, results):
        self.result_table.setRowCount(0)
        self.result_table.setRowCount(len(results))

        for row, candidate in enumerate(results):
            self.result_table.setItem(row, 0, QtWidgets.QTableWidgetItem(candidate['name']))
            self.result_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(candidate['ipk'])))
            self.result_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(candidate['jaringan_komputer'])))
            self.result_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(candidate['bahasa_pemrograman'])))
            self.result_table.setItem(row, 4, QtWidgets.QTableWidgetItem(str(candidate['komunikasi_tim'])))
            self.result_table.setItem(row, 5, QtWidgets.QTableWidgetItem(str(candidate['disiplin_tanggungjawab'])))
            self.result_table.setItem(row, 6, QtWidgets.QTableWidgetItem(f"{candidate['final_score']:.2f}"))
            self.result_table.setItem(row, 7, QtWidgets.QTableWidgetItem(str(candidate['ranking'])))

    def export_to_csv(self):
        options = QtWidgets.QFileDialog.Options()
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(
            self, "Simpan File CSV", "", 
            "CSV Files (*.csv);;All Files (*)", 
            options=options
        )

        if not file_name:
            return

        try:
            results = self.db_manager.get_results()
            with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    'Ranking', 'Nama', 'IPK', 'Jaringan Komputer', 
                    'Bahasa Pemrograman', 'Komunikasi Tim', 
                    'Disiplin & Tanggung Jawab', 'Nilai Akhir'
                ])
                for row in results:
                    writer.writerow([
                        row[8], row[1], row[2], row[3], 
                        row[4], row[5], row[6], f"{row[7]:.2f}"
                    ])
            QtWidgets.QMessageBox.information(self, "Sukses", "Data berhasil diekspor ke CSV.")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Gagal mengekspor data: {str(e)}")
