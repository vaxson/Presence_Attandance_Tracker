from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QHeaderView, QRadioButton, QTableWidgetItem, QWidget 
from services.services import *
from datetime import datetime
import pandas as pd
from services.analytics import user_get_attendance

class Attendance_page(QWidget): 
    def __init__(self):
        super().__init__()
        self.radio_buttons_list=[]
        loader=QUiLoader()
        self.ui=loader.load("ui/attendance_v2.ui")
        # self.ui.lab_table_name.setText("Attendance")
        self.start_date=None
        self.end_date=None
        

        header = self.ui.attendance_table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(1, QHeaderView.ResizeToContents)
        header.setSectionResizeMode(2, QHeaderView.Stretch)
            
        # Calculation Variables
        settings_dictionary=fetch_settings_from_db()
        if(settings_dictionary["success"]) :
            settings=settings_dictionary["result"]
            self.work_duration=settings["work_duration"]
            self.break_duration=settings["break_duration"]
            self.grace_time=settings['grace_time']
            self.min_OT=settings['min_OT_duration']
            self.paid_leaves=settings['paid_leaves']
            self.days_in_month=settings['num_days']
            self.OT_multiplier=settings['OT_multiplier']
            self.salary_method=settings['salary_method']
            self.ot_methord=settings['OT_method']
            self.early_checkout=settings['early_checkout']
            self.enable_payroll=settings['enable_payroll']
        else :
            print(f"Unable to fetch settings form DB (ATT_pg :08)")

        self.layout_sidebar=self.ui.scrollAreaWidgetContents.layout()
        self.ui.btn_cancel.clicked.connect(self.cancel_button_clicked)

        
    def cancel_button_clicked(self) :
        self.ui.close()

    def sync_attendance(self,device) :
        try :
            attendance_list=fetch_attendance_from_device(device=device)
            if(attendance_list["success"]) :
                print("Attendance Fetched")
                push_attendance_to_db(device,attendance_list["result"])
        except Exception as e :
            print(f"Attendance Failed for  {e}")
        
        

    def get_attendance(self,device,settings_object,start_date,end_date) :
        self.start_date=start_date
        self.end_date=end_date
        modelusers=user_get_attendance(device,settings_object,start_date,end_date)
        self.fill_radiobtn(modelusers)
    
    
            

        
    def fill_radiobtn(self,modelusers) :
        for user in modelusers :
            if user.dataFrame["status"].isin(["Full_Day", "Over_Time", "Early_Exit", "Half_Day","Miss_Punch"]).any():
                radio=QRadioButton(user.name)
                radio.modeluser=user
                radio.clicked.connect(self.radio_btn_clicked)
                # self.layout_sidebar.addWidget(radio)
                self.layout_sidebar.insertWidget(self.layout_sidebar.count() - 1, radio)
                

    def radio_btn_clicked(self) :
        
        radio=self.sender()
        user_object=radio.modeluser
        attendance_dataFrame=user_object.dataFrame
        self.ui.user_id.setText(str(user_object.uid))
        self.ui.user_name.setText(str(user_object.name))
        self.ui.from_to.setText(f"{self.start_date.strftime('%d-%m-%y')}   TO   {self.end_date.strftime('%d-%m-%y')}")
        self.ui.attendance_table.setRowCount(len(attendance_dataFrame))
        self.ui.attendance_table.setColumnCount(len(attendance_dataFrame.columns))
        # self.ui.attendance_table.setHorizontalHeaderLabels(attendance_dataFrame.columns)
        row_count=0
        for row in attendance_dataFrame.itertuples() :
            date=row[1].strftime('%d-%m-%y')
            time=round(row[3], 2)
            date=QTableWidgetItem(str(date))
            time=QTableWidgetItem(str(time))
            status=QTableWidgetItem(str(row[2]))
            self.ui.attendance_table.setItem(row_count,0,date)
            self.ui.attendance_table.setItem(row_count,1,time)
            self.ui.attendance_table.setItem(row_count,2,status)
            row_count +=1
        # Defines the length of the table. 
        # Wrong inputs reduces the table visibility
        self.ui.attendance_table.setFixedHeight(row_count*30)
        
        full_days_count=attendance_dataFrame["status"].value_counts()["Full_Day"]
        half_days_count=attendance_dataFrame["status"].value_counts()["Half_Day"]
        early_exit_count=attendance_dataFrame["status"].value_counts()["Early_Exit"]
        over_time_count=attendance_dataFrame["status"].value_counts()["Over_Time"]
        miss_punch_count=attendance_dataFrame["status"].value_counts()["Miss_Punch"]
        absent_count=attendance_dataFrame["status"].value_counts()["Absent"]
        self.ui.present_days.setText(str(full_days_count))
        self.ui.half_days.setText(str(half_days_count))
        self.ui.early_exit.setText(str(early_exit_count))
        self.ui.over_time.setText(str(over_time_count))
        self.ui.miss_punch.setText(str(miss_punch_count))
        self.ui.absent.setText(str(absent_count))

            
            
            
            

                
                