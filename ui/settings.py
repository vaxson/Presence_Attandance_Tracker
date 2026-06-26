from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QTableWidgetItem,QCheckBox,QLineEdit
from PySide6.QtGui import QDoubleValidator
from services.services import fetch_settings_from_db,save_settings_to_db,drop_database_table

class Settings :
    def __init__(self, device_1, device_2):
        self.device_1 = device_1
        self.device_2 = device_2
        self.loader=QUiLoader()
        self.ui=self.loader.load("ui/settings.ui")
        
        # settings Variables
        self.entry_id=1
        self.work_duration=None
        self.break_duration=None
        self.grace_time=None
        self.min_OT_duration=None
        self.paid_leaves=None
        self.days_in_month=None
        self.OT_multiplier=None

        self.salary_methord=None
        self.ot_calculation_method=None
        self.early_checkout=None
        self.enable_payroll=None

        self.validator=QDoubleValidator(0.00, 1000000.00, 2)
        self.ui.work_duration.setValidator(self.validator)
        self.ui.break_duration.setValidator(self.validator)
        self.ui.grace_time.setValidator(self.validator)
        self.ui.min_OT.setValidator(self.validator)
        self.ui.paid_leaves.setValidator(self.validator)
        self.ui.number_of_days.setValidator(self.validator)
        self.ui.ot_multiplier.setValidator(self.validator)

        # callback for buttons
        self.ui.btn_save.clicked.connect(self.save_button_clicked)
        self.ui.btn_cancel.clicked.connect(self.cancel_button_clicked)
        self.ui.btn_format_attendance.clicked.connect(self.format_attendance_db)
        self.ui.btn_format_devices.clicked.connect(self.format_devces_db)
        self.get_valuesdb()
    
    
    def get_valuesdb(self) :
        result=fetch_settings_from_db()
        if(result["success"]):
            settings=result['result']
            self.ui.work_duration.setText(str(settings["work_duration"]))
            self.ui.break_duration.setText(str(settings["break_duration"]))
            self.ui.grace_time.setText(str(settings["grace_time"]))
            self.ui.min_OT.setText(str(settings["min_OT_duration"]))
            self.ui.paid_leaves.setText(str(settings["paid_leaves"]))
            self.ui.number_of_days.setText(str(settings["num_days"]))
            self.ui.ot_multiplier.setText(str(settings["OT_multiplier"]))

            self.work_duration=settings["work_duration"]
            self.break_duration=settings["break_duration"]
            self.grace_time=settings["grace_time"]
            self.min_OT_duration=settings["min_OT_duration"]
            self.paid_leaves=settings["paid_leaves"]
            self.days_in_month=settings["num_days"]
            self.OT_multiplier=settings["OT_multiplier"]
            self.salary_methord=settings["salary_method"]
            if(settings["OT_method"]==1) :
                self.ui.hourly_ot.setChecked(True)
                self.ui.daily_ot.setChecked(False)

                self.ot_calculation_method=True
            else :  
                self.ui.daily_ot.setChecked(True)
                self.ot_calculation_method=False    
            if(settings["early_checkout"]==1) :
                self.ui.early_checkout.setChecked(True)
                self.early_checkout=True
            else :
                self.ui.early_checkout.setChecked(False)
                self.early_checkout=False
            if(settings["enable_payroll"]==1) :
                self.ui.enable_payroll.setChecked(True)
                self.enable_payroll=True
            else :
                self.ui.enable_payroll.setChecked(False)
                self.enable_payroll=False
            if(settings["salary_method"]==1) :
                self.ui.calendar_days.setChecked(True)
                self.ui.working_days.setChecked(False)
                self.salary_method=True
            else :
                self.ui.calendar_days.setChecked(False)
                self.ui.working_days.setChecked(True)
                self.salary_method=False

            
        else :
            print("Error fetching settings from database: ", result["result"])


    
    def save_button_clicked(self) :
        # print(f"Work Duration : {self.ui.work_duration.text()} Break Duration : {self.ui.break_duration.text()} Grace time : {self.ui.grace_time.text()} Minimum OT : {self.ui.min_OT.text()} Paid Leaves : {self.ui.paid_leaves.text()} Number of days : {self.ui.number_of_days.text()} OT Multiplier : {self.ui.ot_multiplier.text()}")
        self.work_duration=int(self.ui.work_duration.text())
        self.break_duration=int(self.ui.break_duration.text())
        self.grace_time=int(self.ui.grace_time.text())
        self.min_OT_duration=float(self.ui.min_OT.text())
        self.paid_leaves=int(self.ui.paid_leaves.text())
        self.days_in_month=int(self.ui.number_of_days.text())
        self.OT_multiplier=float(self.ui.ot_multiplier.text())
        self.salary_method=bool(self.ui.calendar_days.isChecked())
        self.ot_calculation_method=bool(self.ui.hourly_ot.isChecked())
        self.early_checkout=bool(self.ui.early_checkout.isChecked())    
        self.enable_payroll=bool(self.ui.enable_payroll.isChecked())
        save_settings_to_db(self)
        self.get_valuesdb()
        self.cancel_button_clicked()

    def cancel_button_clicked(self) :
        self.ui.close()

    def format_attendance_db(self) :
        drop_database_table(self.device_1,1)
        drop_database_table(self.device_1,2)
        drop_database_table(self.device_2,1)
        drop_database_table(self.device_2,2)
    
    def format_devces_db(self) :
        drop_database_table(self.device_1,3)
        print(f"Format dev clicked")