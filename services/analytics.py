import calendar
import pandas as pd
from datetime import datetime, timedelta
from collections import defaultdict


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
def user_attendance(users_list,start_Date,end_Date):
    for user in users_list :
        if user.dataFrame is not None :
            df=user.dataFrame
            df["timestamp"]=pd.to_datetime(df["timestamp"])
            df.sort_values(by="timestamp", inplace=True)
            df["date"]=df["timestamp"].dt.date
            df["time"]=df["timestamp"].dt.time
            print(df.head())
            
           

'''
            punch_times.sort()
            if len(punch_times) >= 2 :
                first_punch=punch_times[0]
                last_punch=punch_times[-1]
                work_hours=datetime.combine(datetime.min,current_date) + (datetime.combine(datetime.min,last_punch) - datetime.combine(datetime.min,first_punch))
                print(f"Date: {current_date}, Work Hours: {work_hours.time()}")
            else :
                print(f"Date: {current_date}, Insufficient punch data.")
        else :
            print(f"Date: {current_date}, No punch data.")
        current_date += timedelta(days=1)
    '''
    