from PySide6.QtUiTools import QUiLoader 
from services.services import *

class Attendance_page :
    def __init__(self):
        loader=QUiLoader()
        self.ui=loader.load("ui/attendance.ui")
        self.ui.lab_table_name.setText("Attendance")
        self.start_date=None
        self.end_date=None
        

        

    def calculate_attendance(device_id, users_list, self):
        # Fetch attendance data for the specified device and users
        for user in users_list:
           user.attendance_timestamps = fetch_attendance_user_daterange(device_id, user.uid, self.start_date, self.end_date)
        
        # Analyze the attendance data
        analyzed_data = analyze(attendance_data[0], attendance_data[1], attendance_data[2])
        
        # Update the UI with the analyzed attendance data
        self.update_attendance_table(analyzed_data)
        