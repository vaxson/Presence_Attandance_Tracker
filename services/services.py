from device.Zk_device import *
from models.Users import Users
from models.Attendance import Attendance
from database.sqlite_db import *
from services.analytics import *

#Device operations.
def get_device_connection(ipaddress,port_number,device_name) :
    device=Zk_device(ipaddress,port=port_number,timeout=5,device_name=device_name)
    device.Connect()
    return device

def fetch_user_from_device(device):
    users=device.Fetch_users()
    if(users["success"]) :
        modelusers=[]
        for user in users["result"]:
            Modeluser=Users(user.uid,user.name,user.password,device.device_name)
            modelusers.append(Modeluser)
        
        push_user_to_db(modelusers)
        return {"success":True,"result":modelusers}
    
    elif(users["success"]==False) :
        return {"success":False,"result":users["result"]}
    

        

def fetch_attendance_from_device(device) :
    attendance=device.Fetch_attendance()
    modelattendance=[]
    for punch in attendance :
        Modelattendance=Attendance(punch.user_id,punch.timestamp,punch.uid,device.device_name)
        modelattendance.append(Modelattendance)
    return modelattendance


''' Database operations '''
def drop_database_table(device,table_number):
    if table_number==1 :
        table=device.device_name+"_users"
    elif table_number==2 :
        table=device.device_name+"_attendance"
    else :
        print("Invalid table number.")
        return
    drop_table(table)

def create_user_table_for_device(device):
    create_user_tables(device.device_name)

def create_attendance_table_for_device(device):
    create_attendance_tables(device.device_name)

def fetch_attendance_from_db(device):
    rows=fetch_attendance_table(device.device_name)
    for row in rows:
        print(f"User Id: {row[0]}, Name: {row[1]}, Timestamp: {row[2]}")
    return rows

def fetch_users_from_db(device):
    rows=fetch_user_table(device.device_name)
    modelusers=[]
    if(rows["success"]) :
        users=rows["result"]
        for user in users :
            Modeluser=Users(user[0],user[1],user[2],device.device_name)
            try :
                Modeluser.isOtEnabled=user[3]
                Modeluser.salary=user[4]
            except IndexError:
                print("Error occurred while fetching user data from database.")
                print(f"Name : {Modeluser.name}, UID : {Modeluser.uid}, password :{Modeluser.password}, isOtEnabled : {Modeluser.isOtEnabled}, salary : {Modeluser.salary} ")
            modelusers.append(Modeluser)
       
        return {"success":True,"result":modelusers}
    else :
        return {"success":False,"result":rows["result"]}


''''
#fetch only salary and ot information of users from database.
#used to show this data in UI (users Page).
def fetch_users_salary_isOtEnabled_from_db(device) :
    result=fetch_user_salary_isOtEnabled(device.device_name)
    if(result["success"]) :
        return {"success":True,"result":result["result"]}
    else :
        print(f"Error Occured : {result['result']}")
        return {"success":False,"result":result["result"]}
    


'''
def fetch_attendance_user_daterange(device,user_id,start_date,end_date):
    rows=fetch_attendance_user_date_range(device.device_name,user_id,start_date,end_date)
    for row in rows:
        print(f"User Id: {row[0]}, Name: {row[1]}, Timestamp: {row[2]}")
    return rows, start_date,end_date

''' 
* Check if the model user object belong to the same device.
* Make safty.
* Same goes to the push_attendance_to_db methord.
'''
def push_user_to_db(Modeluser):
    try :
        push_user(Modeluser)
        print("User data pushed to database successfully.")
        return True
    except Exception as e:
        print(f"Error occurred while pushing user data to database: {e}")
        return e

def push_attendance_to_db(device,Modelattendance):
    try:
        push_attendance(device,Modelattendance)
        print("Attendance data pushed to database successfully.")
        return True
    except Exception as e:
        print(f"Error occurred while pushing attendance data to database: {e}")
        return e
    

def test_connection(ipaddress,port_number) :
    device_name="Test_Device"
    device=Zk_device(ipaddress,port=port_number,timeout=5,device_name=device_name)
    test_status=device.Connect()

    if(test_status["success"]!= False) :
        device.Disconnect()
        return {"success":True,"status":"Connection successful."}
    else :
        return {"success":False,"status":test_status['object']}
    

def configuration_save(configuration_id,device_name,device_ip,device_port) :
    #save the configuration to database or file
    if(test_connection(device_ip,device_port)['success']) :
        try :
            print(f"Configuration saved for device {device_name} with IP {device_ip} and port {device_port}")
            store_device_information(configuration_id, device_name, device_ip, device_port)
            return {"success":True,"status":"Saved Successfully."}
        except Exception as e:
            return {"success":False,"status":str(e)}
    else :
        return {"success":False,"status":"Failed to save configuration. Cross check the device details."}

def configuration_retrieve_db(configuration_id) :
    #retrieve the configuration from database or file
    try :
        saved_configuration=retrieve_device_information(configuration_id)
        if(saved_configuration) :
            print(f"Configuration retrieved for device {saved_configuration[1]} with IP {saved_configuration[2]} and port {saved_configuration[3]}")
            return {"success":True,"configuration":"saved_configuration"}
        else :
            return {"success":False,"configuration":"No configuration found for the given ID."}
    except Exception as e:
        return {"success":False,"configuration":str(e)}



def analyze(datarows, start_date,end_date) :
    return attendance_analyze(datarows,start_date=start_date,end_date=end_date)