from PySide6.QtUiTools import QUiLoader 
from services.services import *
from services.analytics import user_attendance
import pandas as pd

class Attendance_page :
    def __init__(self):
        loader=QUiLoader()
        self.ui=loader.load("ui/attendance.ui")
        self.ui.lab_table_name.setText("Attendance")
        self.start_date=None
        self.end_date=None
        self.users_list= []

        

    def sync_attendance(self,device) :
        attendance_list=fetch_attendance_from_device(device)
        push_attendance_to_db(device,attendance_list)
                

    def user_get_attendance(self,device,start_date,end_date):
        self.start_date=start_date
        self.end_date=end_date
        # Fetch attendance data for the specified device and users
        self.users_list=fetch_attendance_from_db(device=device)
        for user in self.users_list:
            result=fetch_attendance_user_daterange(device, user.uid, self.start_date, self.end_date)
            if result["success"]:
                user.dataFrame = result["result"]
                print(user.dataFrame.head())


    def calculations(self) :
        for user in self.users_list :
            if user.dataFrame is not None :
                df=user.dataFrame
                df["timestamp"]=pd.to_datetime(df["timestamp"])
                df.sort_values(by="timestamp", inplace=True)
                df["date"]=df["timestamp"].dt.date
                df["time"]=df["timestamp"].dt.time 
                

    def display_attendance(self) :
        user_attendance(self.users_list,self.start_date,self.end_date)
