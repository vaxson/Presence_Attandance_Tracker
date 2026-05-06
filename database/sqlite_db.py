import sqlite3

import pandas as pd
'''
Methords and definitions for database handling and operations.
* __get_dbconnection__() : Establishes a connection to the SQLite database. (INTERNAL USE ONLY)

* create_user_tables(device_name) : Creates a user table for the specified device if it doesn't already exist
.
* create_attendance_tables(device_name) : Creates an attendance table for the specified device if it doesn't already
 exist.
* push_user(Modeluser) : Inserts user data into the corresponding user table in the database.

* push_attendance(Modelattendance) : Inserts attendance data into the corresponding attendance table in the database.

* fetch_attendance_table(device_name) : Fetches attendance data from the corresponding attendance table for the specified device.

* fetch_user_table(device_name) : Fetches user data from the corresponding user table for the specified device.

* drop_table(table) : Drops the specified table from the database.
'''

def __get_dbconnection__():
    db_connection=sqlite3.connect("database/attendance.db")
    return db_connection

#create user table for device
def create_user_tables(device_name):
    User_tablename=device_name+"_users"
    db_connection=__get_dbconnection__()
    cursor=db_connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {User_tablename} (
                        uid INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        password TEXT,
                        isOtEnabled BOOLEAN,
                        salary INTEGER
                    )''')
    db_connection.commit()


#create attendance table for device
def create_attendance_tables(device_name):
    Attendance_tablename=device_name+"_attendance"
    db_connection=__get_dbconnection__()
    cursor=db_connection.cursor()
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {Attendance_tablename} (
                        punch_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NOT NULL,
                        timestamp DATETIME NOT NULL)''')
    db_connection.commit()
    db_connection.close()



#push user data to database
def push_device_user(Modeluser):
    table_name=Modeluser[0].device_name+"_users"
    db_connection=__get_dbconnection__()
    cursor=db_connection.cursor()
    create_user_tables(Modeluser[0].device_name)
    for user in Modeluser :
        cursor.execute(f'''INSERT  INTO {table_name} (uid, name, password,salary,isotenabled) 
                       VALUES (?, ?, ?,?,?) 
                       ON CONFLICT(uid) 
                       DO UPDATE SET name=excluded.name, password=excluded.password''', 
                       (user.uid, user.name, user.password,0,0))
    db_connection.commit()
    db_connection.close()

def push_software_user(Modeluser):
    table_name=Modeluser[0].device_name+"_users"
    db_connection=__get_dbconnection__()
    cursor=db_connection.cursor()
    create_user_tables(Modeluser[0].device_name)
    for user in Modeluser :
        cursor.execute(f'''UPDATE {table_name} 
                       SET isOtEnabled=?, salary=?
                       WHERE uid=?''', (user.isOtEnabled, user.salary, user.uid ))
        
    db_connection.commit()
    db_connection.close()




#push attendance data to database
def push_attendance(device_name,Modelattendance):
    attendance_tablename=Modelattendance[0].device_name+"_attendance"
    db_connection=__get_dbconnection__()
    create_attendance_tables(Modelattendance[0].device_name)
    cursor=db_connection.cursor()

    for attendance in Modelattendance :
        cursor.execute(f'''INSERT OR REPLACE INTO {attendance_tablename}  
                       (punch_id,user_id,timestamp) VALUES(?, ?, ?)''', 
                       (attendance.punchid,attendance.uid,attendance.timestamp))
    db_connection.commit()
    db_connection.close()

#fetching data from database
def fetch_attendance_table(device_name) :
    table_name=device_name+"_attendance"
    print("Fetching attenance......")
    dbconnection=__get_dbconnection__()
    cursor=dbconnection.cursor()
    cursor.execute(f'''SELECT * FROM {table_name}''')
    rows=cursor.fetchall()
    dbconnection.close()
    return rows

#fetching data from database
def fetch_user_table(device_name) :
    try :
        table_name=device_name+"_users"
        print("Fetching users......")
        dbconnection=__get_dbconnection__()
        cursor=dbconnection.cursor()
        cursor.execute(f'''SELECT * FROM {table_name}''')
        rows=cursor.fetchall()
        dbconnection.close()
        return {"success":True,"result":rows}
    except Exception as e :
        return {"success":False,"result":str(e)}


#droping a table from database
def drop_table(table):
    db_connection=__get_dbconnection__()
    cursor=db_connection.cursor()
    print(f"Deleting {table} table.....")
    cursor.execute(f'''DROP TABLE IF EXISTS {table}''')
    db_connection.commit()
    db_connection.close()

def fetch_attendance_date_range(device_name,start_date,end_date) :
    attendance_tablename=device_name+"_attendance"
    user_tablename=device_name+"_users"
    print("Fetching attenance......")
    dbconnection=__get_dbconnection__()


    dataFrame=pd.read_sql(f'''SELECT {attendance_tablename}.punch_id,{attendance_tablename}.user_id ,{user_tablename}.name, 
                                {attendance_tablename}.timestamp FROM {attendance_tablename} 
                                JOIN {user_tablename} ON {attendance_tablename}.user_id
                                  = {user_tablename}.uid 
                                WHERE {attendance_tablename}.timestamp BETWEEN ? AND ?''', 
                                __get_dbconnection__(), params=(start_date,end_date))

    #
    # cursor.execute(f'''SELECT {attendance_tablename}.punch_id,{user_tablename}.name, 
    #                {attendance_tablename}.timestamp FROM {attendance_tablename} 
    #                JOIN {user_tablename} ON {attendance_tablename}.name = {user_tablename}.uid 
    #                WHERE {attendance_tablename}.name={user_id} 
    #                AND {attendance_tablename}.timestamp BETWEEN ? AND ?''', 
    #                (start_date, end_date))
    # dataFrame=cursor.fetchall()

    return dataFrame

def combine_attendance_user() :
    db_connection=__get_dbconnection__()
    cursor=db_connection.cursor()
    cursor.execute(''' SELECT attendance.uid,users.name, attendance.timestamp FROM attendance JOIN users ON attendance.user_id = users.uid''')
    rows=cursor.fetchall()
    db_connection.close()
    print(rows)
    return rows


def store_device_information(device_id,device_name,ip_address,port_number) :
    db_connection=sqlite3.connect("database/devices.db")
    cursor=db_connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS devices (
                        device_id INTEGER PRIMARY KEY,
                        device_name TEXT NOT NULL,
                        ip_address TEXT NOT NULL,
                        port_number INTEGER NOT NULL)''')
    cursor.execute('''INSERT OR REPLACE INTO devices (device_id, device_name, ip_address, port_number) VALUES (?, ?, ?, ?)''', (device_id, device_name, ip_address, port_number))
    db_connection.commit()
    db_connection.close()


def retrieve_device_information(device_id) :
    db_connection=sqlite3.connect("database/devices.db")
    cursor=db_connection.cursor()
    cursor.execute('''SELECT * FROM devices WHERE device_id = ?''', (device_id,))
    rows=cursor.fetchone()
    db_connection.close()
    return rows


