from services.services import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QLabel
from PySide6.QtUiTools import QUiLoader
from ui.users_page import user_page
from utils.helper.ClickFilter import ClickFilter
import resources_rc
from ui.configuration import ConfigurationDevice
from ui.date_selection import Date_selection
from ui.attendance_page import Attendance_page
from threading import Thread

app=QApplication([])
loader=QUiLoader()


# device_list=[]
# device1_ipaddress="169.254.241.222" 
# device1_name="k30"
# device_1=get_device_connection(ipaddress=device1_ipaddress,port_number=4370,device_name=device1_name)


#Configure device objects
configuration_device1=ConfigurationDevice(1)
configuration_device2=ConfigurationDevice(2)
device_1=configuration_device1.device_object
machine1_user_page=user_page(device_1)
machine1_user_page.ui.setEnabled(True)

#Date Selection Objects
date_selection=Date_selection()

#Attendance page object
attendance_page=Attendance_page()

#user_data=fetch_users_from_db(dev1)
#data=fetch_attendance_user_daterange(device_1,5,"2025-02-01 00:00:00","2025-03-01 00:00:00") 
#user_data=analyze(data[0], data[1], data[2])

'''Callback Functions'''
'''
#callback return the status of test connection and update the label in configuration page
def test_connection_status(status, message,configure_ui_id) :
    if(configure_ui_id==1) :
        configuration_device1.ping_status.setText(message)
    elif(configure_ui_id==2) :
        configuration_device2.ping_status.setText(message)
'''

def handle_click(obj) :
    pass

#callback for user button machine 1 and 2
def user_btn_clicked(obj) :
    #drop_database_table(device_1,1)
    name=obj.objectName()
    print(f"Object name: {name}")
    result=Thread(target=fetch_user_from_device, args=(device_1,)).start()

    if(name=="label_users_machine1") :
        if(not result) :
            machine1_user_page.ui.users_label.setText("Device Offline")
        print("Clicked on user machine 1")
        window.stackedwidget_content_area.setCurrentWidget(machine1_user_page.ui)
        machine1_user_page.display_users()
        #Thread(target=fetch_user_from_device, args=(device_1,)).start()
    elif("label_users_machine2" in name) :
        print("Clicked on user machine 2")
    
    print("Exited")
        

#callback for attendance button machine 1 and 2  
def attandance_btn_clicked(obj) :
    name=obj.objectName()
    if("label_attandance_machine1" in name) :
        print(f"Clicked on attendance machine 1") 
        Thread(target=attendance_page.sync_attendance,args=(device_1,)).start()
    
        date_selection.ui.exec()
        start_date=date_selection.start_date
        end_date=date_selection.end_date
        attendance_page.user_get_attendance(device_1,start_date,end_date)


    elif("label_attandance_machine2" in name) :
        print("Clicked on attendance machine 2")
        date_selection.ui.exec()
        start_date=date_selection.start_date
        end_date=date_selection.end_date
    
#callback for configuration button machine 1 and 2
def configuration_btn_clicked(obj) :
    name=obj.objectName()
    if("label_configure_machine1" in name) :
        print("Clicked on configuration machine 1")
        window.stackedwidget_content_area.setCurrentWidget(configuration_device1.ui)
        configuration_device1.ui.machine_name.setText("Machine 1 Configuration")
        Thread(target=device_1.configuration_retrieve).start()

    elif("label_configure_machine2" in name) :
        print("Clicked on configuration machine 2") 
        window.stackedwidget_content_area.setCurrentWidget(configuration_device2.ui)
        configuration_device2.ui.machine_name.setText("Machine 2 Configuration")
        Thread(target=configuration_device2.configuration_retrieve).start()

#callback function for test connection
def test_button_clicked(configuration) :
    configuration.ui.ping_status.setText("Please wait...")
    configuration.ipaddress=configuration_device1.ui.ipaddress.text()
    configuration.portnumber=int(configuration.ui.portnumber.text())
    Thread(target=configuration.test_connection_clicked).start()

def cancel_clicked() :
    window.stackedwidget_content_area.setCurrentWidget(machine1_user_page.ui)

def configuration_save_clicked(configuration) :
    configuration.ui.ping_status.setText("Saving configuration, please wait...")
    Thread(target=configuration.save_clicked).start()
    

#User Page Save button click
def users_save_clicked(users_page) :
    users_page.ui.users_label.setText("Plese wait ")
    Thread(target=users_page.save_user_payroll).start()





# UI actions functions :
def showhide_machineSubbuttons(status) :
    if status :
        window.widget_sub_machine2.setVisible(False)
        window.widget_sub_machine1.setVisible(True)
    else :
        window.widget_sub_machine1.setVisible(True)
        window.widget_sub_machine2.setVisible(False)



#Ui loads


window=loader.load("C:/Users/vaxso/Desktop/Attandance Management system/ui/mainV2.ui")

#machine2_user_page=user_page(device_2).ui
#window.stackedwidget_content_area.addWidget(machine2_user_page)
window.stackedwidget_content_area.addWidget(machine1_user_page.ui)
window.stackedwidget_content_area.addWidget(configuration_device1.ui)
window.stackedwidget_content_area.addWidget(configuration_device2.ui)   
window.widget_sub_machine1.setVisible(False)
window.widget_sub_machine2.setVisible(False)


#clickfilter function to detect click on label and show user data in table
window.clickfilter=ClickFilter(handle_click)
window.users_click=ClickFilter(user_btn_clicked)
window.attendance_click=ClickFilter(attandance_btn_clicked)
window.configuration_click=ClickFilter(configuration_btn_clicked)

#Configuration page Buttons
configuration_device1.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device1))
configuration_device2.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device2))
configuration_device1.ui.btn_cancel.clicked.connect(cancel_clicked)
configuration_device2.ui.btn_cancel.clicked.connect(cancel_clicked)
configuration_device1.ui.btn_save.clicked.connect(lambda: configuration_save_clicked(configuration_device1))
configuration_device2.ui.btn_save.clicked.connect(lambda: configuration_save_clicked(configuration_device2))

#users page buttons
machine1_user_page.ui.Save_button.clicked.connect(lambda:users_save_clicked(machine1_user_page))


window.label_users_machine1.installEventFilter(window.users_click)
window.label_attandance_machine1.installEventFilter(window.attendance_click)
window.label_configure_machine1.installEventFilter(window.configuration_click)
window.label_users_machine2.installEventFilter(window.users_click)
window.label_attandance_machine2.installEventFilter(window.attendance_click)
window.label_configure_machine2.installEventFilter(window.configuration_click)

#Manually asigining device object to label for now, need to find better way to do this.
window.label_attandance_machine1.device=device_1

window.widget_sub_machine1.setVisible(True)
window.widget_sub_machine2.setVisible(True)

#window.rbtn_machine1.toggled.connect(showhide_machineSubbuttons)




'''
table = machine1_user_page.tableWidget
table.horizontalHeader().setVisible(True)
table.horizontalHeader().setFixedHeight(50)
table.setColumnCount(3)
table.setHorizontalHeaderLabels(["Date","Day","Status"])
table.setRowCount(len(user_data))


for user, row in enumerate(user_data):
    
    table.setItem(user, 0, QTableWidgetItem(str(row[0])))
    table.setItem(user, 1, QTableWidgetItem(str(row[1])))
    table.setItem(user, 2, QTableWidgetItem(str(row[2])))

'''

window.show()
app.exec()

