from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QDateEdit, QPushButton, QTableWidget, QTableWidgetItem, QHBoxLayout, QMessageBox
from PyQt5.QtCore import Qt, QDate
import log_manager
from datetime import datetime

class HistoryWindow(QWidget):
    def __init__(self, return_callback):
        super().__init__()

        self.return_callback = return_callback

        self.setWindowTitle("View History Log")
        self.setFixedSize(800, 550)

        layout = QVBoxLayout()

        title = QLabel("Select a date to view the log")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; color: #333333;")
        layout.addWidget(title)

        # sleect date
        self.date_picker = QDateEdit()
        self.date_picker.setDate(QDate.currentDate())
        self.date_picker.setCalendarPopup(True)
        layout.addWidget(self.date_picker)

        self.table = QTableWidget(0, 3)
        self.table.setHorizontalHeaderLabels(["Start Time", "End Time", "Task Description"])
        self.table.horizontalHeader().setStretchLastSection(True) 
        self.table.horizontalHeader().setSectionsMovable(False)
        layout.addWidget(self.table)

        self.total_time_label = QLabel("Total time worked: 0 hours 0 minutes")
        self.total_time_label.setAlignment(Qt.AlignCenter)
        self.total_time_label.setStyleSheet("font-size: 16px; color: #555555;")
        layout.addWidget(self.total_time_label)

        button_layout = QHBoxLayout() # button

        view_button = QPushButton("View Log")
        view_button.clicked.connect(self.view_log)
        button_layout.addWidget(view_button)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.go_back)
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

    def view_log(self):
        selected_date = self.date_picker.date()
        year = selected_date.year()
        month = selected_date.month()
        day = selected_date.day()

        data = log_manager.load_data_for_date(year, month, day)

        self.table.setRowCount(0)  # emtpy out the table
        if data:
            for row_data in data:
                self.add_row(row_data[0], row_data[1], row_data[2])
            self.update_total_time()
        else:
            QMessageBox.information(self, "No Log Found", "No log was found for the selected date.")
            self.total_time_label.setText("Total time worked: 0 hours 0 minutes")

    def add_row(self, start_time, end_time, description):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        self.table.setItem(row_position, 0, QTableWidgetItem(start_time))
        self.table.setItem(row_position, 1, QTableWidgetItem(end_time))
        self.table.setItem(row_position, 2, QTableWidgetItem(description))

    def update_total_time(self):
        total_minutes = 0

        for row in range(self.table.rowCount()):
            start_item = self.table.item(row, 0)
            end_item = self.table.item(row, 1)

            start = start_item.text().strip() if start_item else ""
            end = end_item.text().strip() if end_item else ""

            if start and end:
                try:
                    start_time = datetime.strptime(start, "%H:%M")
                    end_time = datetime.strptime(end, "%H:%M")
                    minutes = (end_time - start_time).total_seconds() / 60
                    if minutes > 0:
                        total_minutes += minutes
                except ValueError:
                    pass 

        hours = int(total_minutes // 60)
        minutes = int(total_minutes % 60)
        self.total_time_label.setText(f"Total time worked: {hours} hours {minutes} minutes")

    def go_back(self):
        self.close()
        self.return_callback()
