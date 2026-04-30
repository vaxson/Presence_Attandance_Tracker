import pandas as pd
class Attendance :
    def __init__(self,user_id,timestamp,punch_id,device_name) :
        self.device_name=device_name
        self.uid=user_id
        self.date=timestamp.date()
        self.time=timestamp.time()
        self.timestamp=timestamp
        self.punchid=punch_id
    