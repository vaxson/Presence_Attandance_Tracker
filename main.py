from services.services import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QLabel
from PySide6.QtUiTools import QUiLoader
from utils.helper.ClickFilter import ClickFilter
import resources_rc
from ui.handlers import *
from threading import Thread



device_list=[]
device1_ipaddress="192.168.1.1" 
device1_name="k30"

device_1=get_device_connection(device1_ipaddress,4730,device1_name)


#device_2=get_device_connection(device_2_ipaddress,device_2_name)


#user_data=fetch_users_from_db(dev1)
data=fetch_attendance_user_daterange(device_1,5,"2025-02-01 00:00:00","2025-03-01 00:00:00") 
user_data=analyze(data[0], data[1], data[2])

'''Callback Functions'''
def handle_click(obj) :
    pass

#callback for user button machine 1 and 2
def user_btn_clicked(obj) :
    name=obj.objectName()
    if("label_user_machine1" in name) :
        print("Clicked on user machine 1")
        window.stackedwidget_content_area.setCurrentWidget(machine1_user_page)
    elif("label_users_machine2" in name) :
        print("Clicked on user machine 2")

#callback for attendance button machine 1 and 2  
def attandance_btn_clicked(obj) :
    name=obj.objectName()
    if("label_attandance_machine1" in name) :
        print("Clicked on attendance machine 1")

    elif("label_attandance_machine2" in name) :
        print("Clicked on attendance machine 2")
    
#callback for configuration button machine 1 and 2
def configuration_btn_clicked(obj) :
    name=obj.objectName()
    if("label_configure_machine1" in name) :
        print("Clicked on configuration machine 1")
        window.stackedwidget_content_area.setCurrentWidget(configuration_device1)
        configuration_device1.machine_name.setText("Machine 1 Configuration")
        

    elif("label_configure_machine2" in name) :
        print("Clicked on configuration machine 2")

#callback function for test connection
def button_clicked(obj) :
    name="btn_test_connection"
    parent=configuration_device1
   
    if(True) :
        if("btn_test_connection" in name) :
            configuration_device1.ping_status.setText("Please wait...")
            Thread(target=test_connection_clicked,args=(device1_ipaddress,4730,update_test_connection_status)).start()

        elif("cancel" in name) :
            pass
        elif("save" in name) :
            pass
        
    elif (parent=="configuration_device_2") :
        pass









# UI actions functions :
def showhide_machineSubbuttons(status):
    if status :
        window.widget_sub_machine2.setVisible(False)
    else :
        window.widget_sub_machine1.setVisible(True  )

app=QApplication([])
loader=QUiLoader()

#Ui loads
configuration_device1=loader.load("ui/configuration.ui")
configuration_device1.device_id=1
window=loader.load("C:/Users/vaxso/Desktop/Attandance Management system/ui/mainV2.ui")
machine1_user_page=loader.load("ui/users.ui")
window.stackedwidget_content_area.addWidget(machine1_user_page)
window.stackedwidget_content_area.addWidget(configuration_device1)
window.frame_analyitics.hide()
window.widget_sub_machine1.setVisible(False)
window.widget_sub_machine2.setVisible(False)


#clickfilter function to detect click on label and show user data in table
window.clickfilter=ClickFilter(handle_click)
window.users_click=ClickFilter(user_btn_clicked)
window.attendance_click=ClickFilter(attandance_btn_clicked)
window.configuration_click=ClickFilter(configuration_btn_clicked)

configuration_device1.btn_test_connection.clicked.connect(button_clicked)

window.label_users_machine1.installEventFilter(window.users_click)
window.label_attandance_machine1.installEventFilter(window.attendance_click)
window.label_configure_machine1.installEventFilter(window.configuration_click)
window.label_users_machine2.installEventFilter(window.users_click)
window.label_attandance_machine2.installEventFilter(window.attendance_click)
window.label_configure_machine2.installEventFilter(window.configuration_click)




label1=window.lab_table_name.setText("Users List")
window.rbtn_machine1.toggled.connect(showhide_machineSubbuttons)





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



window.show()
app.exec()

