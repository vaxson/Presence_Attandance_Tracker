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
