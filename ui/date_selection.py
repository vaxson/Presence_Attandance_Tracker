from PySide6.QtWidgets import QDialog
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QDate
from datetime import datetime, time


class Date_selection(): 
    def __init__(self):
        loader = QUiLoader()
        self.ui = loader.load("ui/date_selection.ui")
        self.start_date = None
        self.end_date = None

        # ── Initial UI state ──
        self.ui.end_date.setEnabled(False)      # hide end_date until start is picked
        self.ui.end_date.setVisible(False)
        self.ui.ok_button.setEnabled(False)     # ok hidden until both dates valid
        self.ui.ok_button.setVisible(False)

        # ── Signals ──
        self.ui.start_date.dateChanged.connect(self.on_start_date_changed)
        self.ui.end_date.dateChanged.connect(self.validate_dates)
        self.ui.ok_button.clicked.connect(self.accep)
        self.ui.cancel_button.clicked.connect(self.rejec)

    def on_start_date_changed(self, date: QDate):
        # Reveal end_date and set its minimum to start_date
        self.ui.end_date.setMinimumDate(date)       # enforces end >= start in the picker itself
        self.ui.end_date.setVisible(True)
        self.ui.end_date.setEnabled(True)

        # If end_date is already set and is now invalid, reset it
        if self.ui.end_date.date() < date:
            self.ui.end_date.setDate(date)

        self.validate_dates()

    def validate_dates(self):
        start = self.ui.start_date.date()
        end = self.ui.end_date.date()

        valid = end >= start  # True when condition is met
        self.ui.ok_button.setVisible(valid)
        self.ui.ok_button.setEnabled(valid)

    def accep(self):
        print("Date selection accepted")
        end_time=time(23, 59, 59)
        self.start_date=datetime(self.ui.start_date.date().year(), self.ui.start_date.date().month(), self.ui.start_date.date().day())
        self.end_date=datetime(self.ui.end_date.date().year(), self.ui.end_date.date().month(), self.ui.end_date.date().day())
        self.end_date=self.end_date.combine(self.end_date, end_time)
        print(f"Start :{self.start_date} | End : {self.end_date}")
        self.ui.accept()
        

    def rejec(self):
        print("Date selection cancelled")
        self.start_date = None
        self.end_date = None
        self.ui.close()