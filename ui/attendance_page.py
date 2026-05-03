from PySide6.QtUiTools import QUiLoader 
from services.services import *
from services.analytics import user_attendance
from datetime import datetime
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
        try :
            attendance_list=fetch_attendance_from_device(device=device)
            push_attendance_to_db(device,attendance_list["result"])
            print("Attendance Fetched")
        except Exception as e :
            print(f"Attendance Failed for  {e}")
        


    def user_get_attendance(self,device,start_date,end_date):
        self.start_date=start_date
        self.end_date=end_date
        # Fetch attendance data for the specified device and users
        # self.users_list=fetch_users_from_db(device=device)
        # self.users_list=self.users_list["result"]
        # for users in self.users_list :
        result=fetch_attendance_daterange(device,self.start_date,self.end_date)  
        users=fetch_users_from_db(device=device)
        self.users_list=users["result"]

        if result["success"]:
            dataFrame = result["result"]
            print(dataFrame.head())
            dataFrame["timestamp"]=pd.to_datetime(dataFrame["timestamp"])
            dataFrame["date"]=dataFrame["timestamp"].dt.date
            dataFrame["time"]=dataFrame["timestamp"].dt.time
            for user in self.users_list :
                user.dataFrame=dataFrame[dataFrame["name"]==user.name]
            self.calculations()

        

    def calculations(self) :
        for user in self.users_list :
            print(f"user Name : {user.name}")
        
        # groupddataFrame=dataFrame.groupby("name")
        # for key,df in groupddataFrame :
        #     print(f"User : {key}")
        #     df["timestamp"]=pd.to_datetime(df["timestamp"])
        #     # df.sort_values(by="timestamp", inplace=True)
        #     df["date"]=df["timestamp"].dt.date
        #     df["time"]=df["timestamp"].dt.time 
            print(user.dataFrame.head())
                

    def display_attendance(self) :
        user_attendance(self.users_list,self.start_date,self.end_date)
