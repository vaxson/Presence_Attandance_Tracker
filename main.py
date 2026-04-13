from services.services import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QLabel
from PySide6.QtUiTools import QUiLoader
from utils.helper.ClickFilter import ClickFilter
import resources_rc
from ui.configuration import ConfigurationDevice
from threading import Thread

app=QApplication([])
loader=QUiLoader()


device_list=[]
device1_ipaddress="192.168.1.1" 
device1_name="k30"

device_1=get_device_connection(device1_ipaddress,4730,device1_name)

#Configure device objects
configuration_device1=ConfigurationDevice(1)
configuration_device2=ConfigurationDevice(2)

#user_data=fetch_users_from_db(dev1)
data=fetch_attendance_user_daterange(device_1,5,"2025-02-01 00:00:00","2025-03-01 00:00:00") 
user_data=analyze(data[0], data[1], data[2])

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
        window.stackedwidget_content_area.setCurrentWidget(configuration_device1.ui)
        configuration_device1.ui.machine_name.setText("Machine 1 Configuration")
    elif("label_configure_machine2" in name) :
        print("Clicked on configuration machine 2") 
        window.stackedwidget_content_area.setCurrentWidget(configuration_device2.ui)
        configuration_device2.ui.machine_name.setText("Machine 2 Configuration")

#callback function for test connection
def test_button_clicked(configuration) :
    configuration.ui.ping_status.setText("Please wait...")
    configuration.ipaddress=configuration_device1.ui.ipaddress.text()
    configuration.portnumber=int(configuration.ui.portnumber.text())
    Thread(target=configuration.test_connection_clicked).start()

def cancel_clicked() :
    window.stackedwidget_content_area.setCurrentWidget(machine1_user_page)
    

        





# UI actions functions :
def showhide_machineSubbuttons(status):
    if status :
        window.widget_sub_machine2.setVisible(False)
        window.widget_sub_machine1.setVisible(True)
    else :
        window.widget_sub_machine1.setVisible(True)
        window.widget_sub_machine2.setVisible(False)



#Ui loads


window=loader.load("C:/Users/vaxso/Desktop/Attandance Management system/ui/mainV2.ui")
machine1_user_page=loader.load("ui/users.ui")
window.stackedwidget_content_area.addWidget(machine1_user_page)
window.stackedwidget_content_area.addWidget(configuration_device1.ui)
window.stackedwidget_content_area.addWidget(configuration_device2.ui)
window.frame_analyitics.hide()
window.widget_sub_machine1.setVisible(False)
window.widget_sub_machine2.setVisible(False)


#clickfilter function to detect click on label and show user data in table
window.clickfilter=ClickFilter(handle_click)
window.users_click=ClickFilter(user_btn_clicked)
window.attendance_click=ClickFilter(attandance_btn_clicked)
window.configuration_click=ClickFilter(configuration_btn_clicked)

configuration_device1.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device1))
configuration_device2.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device2))
configuration_device1.ui.btn_cancel.clicked.connect(cancel_clicked)
configuration_device2.ui.btn_cancel.clicked.connect(cancel_clicked)


window.label_users_machine1.installEventFilter(window.users_click)
window.label_attandance_machine1.installEventFilter(window.attendance_click)
window.label_configure_machine1.installEventFilter(window.configuration_click)
window.label_users_machine2.installEventFilter(window.users_click)
window.label_attandance_machine2.installEventFilter(window.attendance_click)
window.label_configure_machine2.installEventFilter(window.configuration_click)

window.widget_sub_machine1.setVisible(True)
window.widget_sub_machine2.setVisible(True)


label1=window.lab_table_name.setText("Users List")
#window.rbtn_machine1.toggled.connect(showhide_machineSubbuttons)





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

