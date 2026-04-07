from services.services import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QLabel
from PySide6.QtUiTools import QUiLoader
from utils.helper.ClickFilter import ClickFilter
import resources_rc

print("Enter IP address of the device : ")
ipaddress="169.254.241.222"
dev1=get_device_connection(ipaddress,"k30")
#user_data=fetch_users_from_db(dev1)
data=fetch_attendance_user_daterange(dev1,5,"2025-02-01 00:00:00","2025-03-01 00:00:00") 
user_data=analyze(data[0], data[1], data[2])

'''Callback Functions'''

def handle_click(obj):
    print("Clicked on : ",obj.objectName())
    if(obj.objectName()=="lable_user_machine1"):
        print("Clicked on user machine 1")
        window.stackedwidget_content_area.addWidget(machine1_user_page)
        window.stackedwidget_content_area.setCurrentWidget(machine1_user_page)
        window.frame_analyitics.setVisible(True)

    if(obj.objectName()=="lable_machine1_configure"):
        print("Clicked on machine 1 configure")
        window.stackedwidget_content_area.addWidget(machine1_configuration)
        window.stackedwidget_content_area.setCurrentWidget(machine1_configuration)

#callback for user button machine 1 and 2
def user_btn_clicked(obj) :
    if(obj.objectName()=="label_user_machine1") :
        print("Clicked on user machine 1")
    elif(obj.objectName=="label_users_machine2") :
        print("Clicked on user machine 2")

#callback for attendance button machine 1 and 2  
def attandance_btn_clicked(obj) :
    if(obj.objectName()=="label_attandance_machine1") :
        print("Clicked on attendance machine 1")
    elif(obj.objectName()=="label_attandance_machine2") :
        print("Clicked on attendance machine 2")
    
#callback for configuration button machine 1 and 2
def configuration_btn_clicked(obj) :
    if(obj.objectName()=="label_configure_machine1") :
        print("Clicked on configuration machine 1")
    elif(obj.objectName()=="label_configure_machine2") :
        print("Clicked on configuration machine 2")






# UI actions functions :
def showhide_machineSubbuttons(status):
    if status :
        window.widget_sub_machine2.setVisible(False)
    else :
        window.widget_sub_machine1.setVisible(True  )

app=QApplication([])
loader=QUiLoader()
window=loader.load("C:/Users/vaxso/Desktop/Attandance Management system/ui/mainV2.ui")
window.frame_analyitics.hide()
window.widget_sub_machine1.setVisible(False)

#clickfilter function to detect click on label and show user data in table
window.clickfilter=ClickFilter(handle_click)
window.users_click=ClickFilter(user_btn_clicked)
window.attendance_click=ClickFilter(attandance_btn_clicked)
window.configuration_click=ClickFilter(configuration_btn_clicked)

window.label_users_machine1.installEventFilter(window.users_click)
window.label_attandance_machine1.installEventFilter(window.attendance_click)
window.label_configure_machine1.installEventFilter(window.configuration_click)
window.label_users_machine2.installEventFilter(window.users_click)
window.label_attandance_machine2.installEventFilter(window.attendance_click)
window.label_configure_machine2.installEventFilter(window.configuration_click)



label1=window.lab_table_name.setText("Users List")
window.rbtn_machine1.toggled.connect(showhide_machineSubbuttons)

machine1_user_page=loader.load("ui/users.ui")
machine1_configuration=loader.load("ui/configuration.ui")


table=machine1_user_page.tableWidget
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

