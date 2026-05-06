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
                print(f"user Name : {user.name}")
                user.dataFrame=dataFrame[dataFrame["name"]==user.name]
                all_date=all_dates.merge(user.dataFrame,on="date",how="left").sort_values(["date","time"])
                # print(all_date)
                self.calculations(all_date)
                

           



    def calculations(self,user_dataFrame) :
        first_punch=0
        last_punch=0
        work_hours=0
        aggregate_dataFrame=user_dataFrame.groupby("date")["time"].agg("count").reset_index()
        for aggregate in aggregate_dataFrame.itertuples() :
            if(aggregate.time == 0) :
                print(f"{aggregate.date} : Absent ")
                continue
            elif(aggregate.time %2 ==0) :
                for user_DF in user_dataFrame[user_dataFrame['date']==aggregate.date].itertuples() :
                    if(first_punch==0):
                        first_punch=user_DF.timestamp
                    else :
                        last_punch=user_DF.timestamp
                        total_seconds = (last_punch - first_punch).total_seconds()
                        hours = total_seconds / 3600
                        work_hours=work_hours+hours
                        first_punch=0
                        last_punch=0
                print(f"Date {aggregate.date} | Present | Work Duration :{work_hours}")
                work_hours=0

                
                
            elif(aggregate.time %2 > 0) :
                print(f"Date {aggregate.date} | Present, Miss punch")
        
        
            # print(f"Date :{aggregate.date} | Count : {aggregate.time}")
        #aggregate_dataFrame=aggregate_dataFrame["date"]
        # print(aggregate_dataFrame)
        # for x in user_dataFrame.itertuples():
        #     print(f"date: {x.time[0]} : {x.time[-1]}")

        # work_hours=0
        # time_length=len(user_dataFrame["time"])
        # print(f"Time lngth : {time_length}")
        # if time_length==0:
        #     print(f"{user_dataFrame['date']} | Absent")
        #     return None
        # elif time_length % 2 >0 :
        #     print(f"{user_dataFrame['date']} :Present | MISS PUNCH")
        #     return None
        # elif time_length %2==0 :
        #     for index in range(0,time_length,2):
        #         in_punch=user_dataFrame["time"][index]
        #         out_punch=user_dataFrame["time"][index+1]
        #         duration=out_punch-in_punch  
        #         work_hours=work_hours+duration
        #     print(f"{user_dataFrame['date']}: present : Hours {work_hours}")
                
            
       
            

        
    def display_attendance(self) :
        user_attendance(self.users_list,self.start_date,self.end_date)
 