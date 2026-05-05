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
            if(attendance_list["success"]) :
                print("Attendance Fetched")
                push_attendance_to_db(device,attendance_list["result"])
        except Exception as e :
            print(f"Attendance Failed for  {e}")
        
        


    def user_get_attendance(self,device,start_date,end_date):
        self.start_date=start_date
        self.end_date=end_date
        all_dates=pd.date_range(self.start_date,self.end_date)
        all_dates=pd.DataFrame({"date" : all_dates})
        # Fetch attendance data for the specified device and users
        # self.users_list=fetch_users_from_db(device=device)
        # self.users_list=self.users_list["result"]
        # for users in self.users_list :
        result=fetch_attendance_daterange(device,self.start_date,self.end_date)  
        users=fetch_users_from_db(device=device)
        self.users_list=users["result"]
        if result["success"]:
            dataFrame = result["result"]
            dataFrame["timestamp"]=pd.to_datetime(dataFrame["timestamp"])
            dataFrame=dataFrame.sort_values("timestamp")
            dataFrame["date"]=dataFrame["timestamp"].dt.floor("D")
            dataFrame["time"]=dataFrame["timestamp"].dt.time
            for user in self.users_list :
                user.dataFrame=dataFrame[dataFrame["name"]==user.name]
                user.dataFrame=user.dataFrame.groupby("date")["time"].apply(list).reset_index()
                all_date=all_dates.merge(user.dataFrame,on="date",how="left")
                print(all_date.head())

                # print(f"user Name :{user.name}")
           


        

    def calculations(self,attendanceFrame) :
        work_hours=0
        for punches in attendanceFrame :
            punch_size=len(punches)
            if(punch_size%2==0):
                for punch in punches :
                    work_hours=work_hours+punch
                print(work_hours)
            # elif punch_size<=0:
            #     # print(f"{date} : absent")
            # else :
            #     pass
            #     # print(f"{date} :present miss punch")
            #     pass
    
            

        
    def display_attendance(self) :
        user_attendance(self.users_list,self.start_date,self.end_date)
