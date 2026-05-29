import calendar
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict
from services.services import fetch_attendance_daterange,fetch_users_from_db
from collections import defaultdict



# work_duration=settings.work_duration
# break_duration=settings.break_duration
# grace_time=settings.grace_time
# min_OT=settings.min_OT_duration
# paid_leaves=settings.paid_leaves
# days_in_month=settings.days_in_month
# OT_multiplier= settings.OT_multiplier
# salary_method=settings.salary_method
# ot_methord=settings.ot_calculation_method
# early_checkout=settings.early_checkout
# enable_payroll=settings.enable_payroll


def attendance_analyze(database_rows,start_date,end_date) :
    date_punch_dictionary=defaultdict(list)
    for rows in database_rows :
        datetme=datetime.strptime(rows[2],"%Y-%m-%d %H:%M:%S")
        Date=datetme.date()
        date_punch_dictionary[Date].append(datetme.time())
    return work_hours_calculation(date_punch_dictionary,start_date,end_date)


def work_hours_calculation(date_punch_dictionary,start_date,end_date) :
    data_row=[]
    start_date=datetime.strptime(start_date,"%Y-%m-%d %H:%M:%S").date()
    end_date=datetime.strptime(end_date,"%Y-%m-%d %H:%M:%S").date()  
    current_date=start_date
    while current_date <= end_date :
        if current_date in date_punch_dictionary :
            punch_times=len(date_punch_dictionary[current_date])
            if punch_times%2==0 :
                print(f"{current_date} {current_date.strftime('%A')}, Status : Present")
                row=[str(current_date),current_date.strftime('%A'),"Present"]
                data_row.append(row)
            else :
                print(f"{current_date} {current_date.strftime('%A')}, Status : present Missing Punch")
                row=[str(current_date),current_date.strftime('%A'),"Present Missing Punch"]
                data_row.append(row)
        else :
            print(f"{current_date} {current_date.strftime('%A')}, Status : Absent")
            row=[str(current_date),current_date.strftime('%A'),"Absent"]
            data_row.append(row)

        current_date += timedelta(days=1)
    return data_row

# ------------------------------------------------------------------------------------------------------------------------
# using dataframe from pandas

def user_get_attendance(device,settings,start_date,end_date):
    modelusers=[]
    settings.get_valuesdb()
    all_dates=pd.date_range(start_date,end_date)
    all_dates=pd.DataFrame({"date" : all_dates})
    # Fetch attendance data for the specified device and users
   
    # for users in self.users_list :
   
    result=fetch_attendance_daterange(device,start_date,end_date)  
    users=fetch_users_from_db(device=device)
    users_list=users["result"]
    if result["success"]:
        dataFrame = result["result"]
        dataFrame["timestamp"]=pd.to_datetime(dataFrame["timestamp"])
        dataFrame=dataFrame.sort_values("timestamp")
        dataFrame["date"]=dataFrame["timestamp"].dt.floor("D")
        dataFrame["time"]=dataFrame["timestamp"].dt.time
        for user in users_list :
            print(f"user Name : {user.name}")
            user.dataFrame=dataFrame[dataFrame["name"]==user.name]
            all_date=all_dates.merge(user.dataFrame,on="date",how="left").sort_values(["date","time"])
            # print(f"USR DF {user.dataFrame}")
            # print(f"All Dates : {all_dates}")
            # print(f"ALl DATE : {all_date}")
            # print(all_date.groupby('date')["time"].agg("count").reset_index())
            user.dataFrame=all_date
            modelusers.append(calculations(settings, user))
        return modelusers
    else :
        print(f"Error fetching attendance data: {result['result']}")
        return None
    





def calculations(settings,user_object) :
    user_dataFrame=user_object.dataFrame
    first_punch=0
    last_punch=0
    work_hours=0
    

    # settings variables
    work_duration=settings.work_duration
    break_duration=settings.break_duration
    grace_time=settings.grace_time
    min_OT=settings.min_OT_duration
    
    # Attendance calculation variables
    minimum_duration=2.5
    full_duration=None
    half_duration=None

    aggregate_dataFrame=user_dataFrame.groupby("date")["time"].agg("count").reset_index()
    # Iterates over each dates
    for aggregate in aggregate_dataFrame.itertuples() :
        
        
        status=None
        # print(f"Aggregate : {aggregate}")
        if(aggregate.time == 0) :
            # print(f"{aggregate.date} : Absent ")
            aggregate_dataFrame.loc[aggregate.Index,"status"]="Absent"
            aggregate_dataFrame.loc[aggregate.Index,"hours"]=0
            continue
        
        # Even punches for valid punches
        elif(aggregate.time %2 ==0) :
            # counting each punches for the date and calculating work hours
            for user_DF in user_dataFrame[user_dataFrame['date']==aggregate.date].itertuples() :
                if(first_punch==0):
                    first_punch=user_DF.timestamp
                else :
                    last_punch=user_DF.timestamp
                    total_seconds = (last_punch - first_punch).total_seconds()
                    hours = total_seconds / 3600
                    work_hours=round(work_hours+hours,2)
                    first_punch=0
                    last_punch=0

            if(aggregate.time ==2):
                full_duration=work_duration + break_duration
                half_duration=full_duration/2
                if(work_hours < minimum_duration) :
                    status="Absent"
                elif(work_hours >= minimum_duration and work_hours < half_duration) :
                    status="Half_Day"
                elif(work_hours >  half_duration and work_hours < full_duration -grace_time):
                    status="Early_Exit"
                elif(work_hours > full_duration-grace_time and work_hours < full_duration+ min_OT):
                    status="Full_Day"
                elif(work_hours> full_duration + min_OT):
                    status="Over_Time"

            elif(aggregate.time >2):
                full_duration=work_duration 
                half_duration=full_duration/2
                if(work_hours < minimum_duration) :
                    status="Absent"
                elif(work_hours > minimum_duration and work_hours < half_duration) :
                    status="Half_Day"
                elif( work_hours > half_duration  and work_hours < full_duration-grace_time):
                    status="Early_Exit"
                elif(work_hours >= (full_duration -grace_time) and work_hours < (full_duration + min_OT)):
                    status="Full_Day"
                elif(work_hours >= (full_duration + min_OT)):
                    status="Over_Time"

            # print(f"Check : {user_dataFrame.groupby('date')['time'].apply(list)}")
            hours=int(work_hours)
            minutes=round(60*(work_hours%1))
            aggregate_dataFrame.loc[aggregate.Index,"status"]=status
            aggregate_dataFrame.loc[aggregate.Index,"hours"]=hours+minutes/100
            # print(f"index :{aggregate.Index} Date {aggregate.date} | Present |RAW Work: {work_hours} Work Duration :{hours+(minutes/100)} | {status}")
            work_hours=0
        
        # ODD PUNCHES FOR MISS PUNCH
        elif(aggregate.time %2 > 0) :
            # print(f"Date {aggregate.date} | Present, Miss punch")
            aggregate_dataFrame.loc[aggregate.Index,"status"]="Miss_Punch"
            aggregate_dataFrame.loc[aggregate.Index,"hours"]=0
            continue
        
    user_dataFrame=aggregate_dataFrame[["date","status","hours"]]
    user_object.dataFrame=user_dataFrame
    # print(f"User Attendance : {user_object.dataFrame}")
    # print(f"User Aggregate : {aggregate_dataFrame}")
    return user_object


def report_generation(settings):
    # settings variables
    paid_leaves=settings.paid_leaves
    days_in_month=settings.days_in_month
    OT_multiplier= settings.OT_multiplier
    salary_method=settings.salary_method
    ot_methord=settings.ot_calculation_method
    early_checkout=settings.early_checkout
    enable_payroll=settings.enable_payroll
