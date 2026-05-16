from PySide6.QtUiTools import QUiLoader 
from PySide6.QtWidgets import QTableWidgetItem,QCheckBox,QLineEdit
from PySide6.QtGui import QDoubleValidator
from services.services import fetch_settings_from_db,save_settings_to_db

class Settings :
    def __init__(self):
        self.loader=QUiLoader()
        self.ui=self.loader.load("ui/settings.ui")
        
        # settings Variables
        self.entry_id=1
        self.two_punch_duration=None
        self.four_punch_duration=None
        self.grace_time=None
        self.min_OT_duration=None
        self.paid_leaves=None
        self.days_in_month=None
        self.OT_multiplier=None
        self.ot_calculation_method=None
        self.early_checkout=None
        self.enable_payroll=None

        self.validator=QDoubleValidator(0.00, 1000000.00, 2)
        self.ui.duration_2_punch.setValidator(self.validator)
        self.ui.duration_4_punch.setValidator(self.validator)
        self.ui.grace_time.setValidator(self.validator)
        self.ui.min_OT.setValidator(self.validator)
        self.ui.paid_leaves.setValidator(self.validator)
        self.ui.number_of_days.setValidator(self.validator)
        self.ui.ot_multiplier.setValidator(self.validator)

        # callback for buttons
        self.ui.btn_save.clicked.connect(self.save_button_clicked)
        self.ui.btn_cancel.clicked.connect(self.cancel_button_clicked)
        self.get_valuesdb()
    
    
    def get_valuesdb(self) :
        result=fetch_settings_from_db()
        if(result["success"]):
            settings=result['result']
            self.ui.duration_2_punch.setText(str(settings["2_punch"]))
            self.ui.duration_4_punch.setText(str(settings["4_punch"]))
            self.ui.grace_time.setText(str(settings["grace_time"]))
            self.ui.min_OT.setText(str(settings["min_OT_duration"]))
            self.ui.paid_leaves.setText(str(settings["paid_leaves"]))
            self.ui.number_of_days.setText(str(settings["num_days"]))
            self.ui.ot_multiplier.setText(str(settings["OT_multiplier"]))

            self.two_punch_duration=settings["2_punch"]
            self.four_punch_duration=settings["4_punch"]
            self.grace_time=settings["grace_time"]
            self.min_OT_duration=settings["min_OT_duration"]
            self.paid_leaves=settings["paid_leaves"]
            self.days_in_month=settings["num_days"]
            self.OT_multiplier=settings["OT_multiplier"]
            
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

            
        else :
            print("Error fetching settings from database: ", result["result"])


    
    def save_button_clicked(self) :
        print(f"Duration for 2 punch : {self.ui.duration_2_punch.text()} Duration for 4 punch : {self.ui.duration_4_punch.text()} Grace time : {self.ui.grace_time.text()} Minimum OT : {self.ui.min_OT.text()} Paid Leaves : {self.ui.paid_leaves.text()} Number of days : {self.ui.number_of_days.text()} OT Multiplier : {self.ui.ot_multiplier.text()}")
        self.two_punch_duration=int(self.ui.duration_2_punch.text())
        self.four_punch_duration=int(self.ui.duration_4_punch.text())
        self.grace_time=int(self.ui.grace_time.text())
        self.min_OT_duration=int(self.ui.min_OT.text())
        self.paid_leaves=int(self.ui.paid_leaves.text())
        self.days_in_month=int(self.ui.number_of_days.text())
        self.OT_multiplier=float(self.ui.ot_multiplier.text())
        self.ot_calculation_method=bool(self.ui.hourly_ot.isChecked())
        self.early_checkout=bool(self.ui.early_checkout.isChecked())    
        self.enable_payroll=bool(self.ui.enable_payroll.isChecked())
        save_settings_to_db(self)

    def cancel_button_clicked(self) :
        self.ui.close()