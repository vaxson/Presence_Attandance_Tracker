from PySide6.QtWidgets import QCheckBox, QLineEdit, QTableWidgetItem,QLabel,QFrame,QDateEdit,QDialog
from PySide6.QtUiTools import QUiLoader 
from datetime import datetime,time

class Date_selection(QDialog):
    def __init__(self) :
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load("ui/date_selection.ui")
        self.start_date=None
        self.end_date=None
        self.ui.ok_button.clicked.connect(self.ok_button_clicked)
        self.ui.cancel_button.clicked.connect(self.rejection)

    def ok_button_clicked(self) :
        self.start_date=self.ui.start_date.date()
        self.end_date=self.ui.end_date.date()

    def rejection(self):
        print("Date selection cancelled")
        super().reject()


class Date_selection():
    def __init__(self) :
        super().__init__()
        loader=QUiLoader()
        self.ui=loader.load("ui/date_selection.ui")
        self.start_date=None
        self.end_date=None
        
        self.ui.cancel_button.clicked.connect(self.reject)
        self.ui.ok_button.clicked.connect(self.accept)

    def accept(self) :
        end_time=time(23, 59, 59)
        self.start_date=datetime(self.ui.start_date.date().year(), self.ui.start_date.date().month(), self.ui.start_date.date().day())
        self.end_date=datetime(self.ui.end_date.date().year(), self.ui.end_date.date().month(), self.ui.end_date.date().day())
        self.end_date=self.end_date.combine(self.end_date, end_time)
        self.ui.accept()

    def reject(self):
        print("Date selection cancelled")
        self.ui.reject()        # have absolutly no idea how it works!!!