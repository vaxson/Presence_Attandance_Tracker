from services.services import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QLabel
from PySide6.QtUiTools import QUiLoader
from ui.users_page import user_page
from utils.helper.ClickFilter import ClickFilter
import resources_rc
from ui.settings import Settings
from ui.configuration import ConfigurationDevice
from ui.date_selection import Date_selection
from ui.attendance_page import Attendance_page
from threading import Thread
from utils.helper.PyInstaller_helper import resource_path
# resource_path=PyInstaller_helper.resource_path
app=QApplication([])
loader=QUiLoader()


# device_list=[]
# device1_ipaddress="169.254.241.222" 
# device1_name="k30"
# device_1=get_device_connection(ipaddress=device1_ipaddress,port_number=4370,device_name=device1_name)


loading_page = loader.load(resource_path("ui/loading_page.ui"))
loading_page.show()
app.processEvents()

class initialization() :
    def __init__(self) :
        self.configuration_device2=ConfigurationDevice(2)
        self.configuration_device1=ConfigurationDevice(1)
         # settings page object
        #Date Selection Objects
        self.date_selection=Date_selection()
        self.init_machine1()
        self.init_machine2()
        self.settings_page_init()
        
    def init_machine1(self) :
    #Configure device objects
        print("MAchine 1 init done")
        # self.device_1=self.configuration_device1.device_object
        self.machine1_user_page=user_page(self.configuration_device1.device_object)
        self.machine1_user_page.ui.setEnabled(True)
        
    def init_machine2(self) :
        print("MAchine 2 init done")
        # self.device_2=self.configuration_device2.device_object
        self.machine2_user_page=user_page(self.configuration_device2.device_object)
        self.machine2_user_page.ui.setEnabled(True)
    
    def settings_page_init(self) :
        self.settings_page=Settings(self.configuration_device1.device_object,self.configuration_device2.device_object)

init=initialization()
# #Configure device objects
# configuration_device1=ConfigurationDevice(1)
# configuration_device2=ConfigurationDevice(2)
# device_1=configuration_device1.device_object
# device_2=configuration_device2.device_object
# machine1_user_page=user_page(device_1)
# machine1_user_page.ui.setEnabled(True)
# machine2_user_page=user_page(device_2)
# machine2_user_page.ui.setEnabled(True)
# # settings page object
# settings_page=Settings(device_1,device_2)

# #Date Selection Objects
# date_selection=Date_selection()


#Attendance page object
# attendance_page=Attendance_page()

#user_data=fetch_users_from_db(dev1)
#data=fetch_attendance_user_daterange(device_1,5,"2025-02-01 00:00:00","2025-03-01 00:00:00") 
#user_data=analyze(data[0], data[1], data[2])

'''Callback Functions'''
'''
#callback return the status of test connection and update the label in configuration page
def test_connection_status(status, message,configure_ui_id) :
    if(configure_ui_id==1) :
        configuration_device1.ui.status.setText(message)
    elif(configure_ui_id==2) :
        configuration_device2.ui.status.setText(message)
'''
def check_stauts() :
    Thread(target=init.configuration_device1.checkstatus).start()
    Thread(target=init.configuration_device2.checkstatus).start()
    # if(configuration_device1.isonline) :
    #     window.rbtn_machine1.styleSheet("""
    #                 QRadioButton {
    #                         border: 0px solid #4a4a6a;
    #                     }
    #                 """)
    # if(configuration_device2.isonline) :
    #     window.rbtn_machine2.styleSheet("""
    #                 QRadioButton {
    #                         border: 0px solid #4a4a6a;
    #                     }
    #                 """)

check_stauts()

def syncMachine(device,attendance_page) :
    print("00%")
    window.progressBar.setVisible(True)
    try :
        fetch_user_from_device(device)
    except Exception as e :
        return e
    window.progressBar.setValue(50)
    print("50%")
    if(attendance_page) :
        try :
            attendance_page.sync_attendance(device)
        except Exception as e :
            return e
    window.progressBar.setValue(100)
    print("100%")
    window.progressBar.setVisible(False)
    return True 

        
        
#callback for user button machine 1 and 2
def user_btn_clicked(obj) :
    check_stauts()
    #drop_database_table(device_1,1)
    name=obj.objectName()
    print(f"Object name: {name}")
    # Selection for machine 1
    if(name=="label_users_machine1") :
        print("Clicked on user machine 1")
        if(init.configuration_device1.isonline) :
            init.machine1_user_page.ui.users_label.setText("Device Online")
            syncMachine(init.configuration_device1.device_object,None)
        else :
            init.machine1_user_page.ui.users_label.setText("Device Offline")
        window.stackedwidget_content_area.setCurrentWidget(init.machine1_user_page.ui)
        init.machine1_user_page.display_users()

    #Selection for machine 2 
    elif name == "label_users_machine2":
        print("Clicked on user machine 2")
         #   Display the online status of the device in the user page label
        if(init.configuration_device2.isonline) :
            init.machine2_user_page.ui.users_label.setText("Device Online")
            syncMachine(init.configuration_device2.device_object,None)
        else :
            init.machine2_user_page.ui.users_label.setText("Device Offline")
        window.stackedwidget_content_area.setCurrentWidget(init.machine2_user_page.ui)
        init.machine2_user_page.display_users()
    print("Exited")
        

#callback for attendance button machine 1 and 2  
def attandance_btn_clicked(obj) :
    check_stauts()
    window.attendance_page=Attendance_page()
    attendance_page=window.attendance_page
    name=obj.objectName()
    if(name== "label_attandance_machine1") :
        print(f"Clicked on attendance machine 1") 
        if(init.configuration_device1
           
           .isonline) :
            # syncMachine(init.device_2,None)
            syncMachine(init.configuration_device1.device_object,attendance_page)
    
        init.date_selection.ui.exec()
        start_date=init.date_selection.start_date
        end_date=init.date_selection.end_date
        if(start_date !=None and end_date !=None) :
            attendance_page.get_attendance(init.configuration_device1.device_object,init.settings_page,start_date,end_date)
            attendance_page.ui.show()
        else :
            print("invalid date selection")
        

    elif(name == "label_attandance_machine2") :
        print("Clicked on attendance machine 2")
        if(init.configuration_device2.isonline) :
            syncMachine(init.configuration_device2.device_object,attendance_page)

        init.date_selection.ui.exec()
        start_date=init.date_selection.start_date
        end_date=init.date_selection.end_date
        if(start_date !=None and end_date !=None) :
            attendance_page.get_attendance(init.configuration_device2.device_object,init.settings_page,start_date,end_date)
            attendance_page.ui.show()
        else :
            print("invalid date selection")
    # attendance_page=Attendance_page()

    
#callback for configuration button machine 1 and 2
def configuration_btn_clicked(obj) :
    check_stauts()
    name=obj.objectName()
    if(name== "label_configure_machine1") :
        print("Clicked on configuration machine 1")
        window.stackedwidget_content_area.setCurrentWidget(init.configuration_device1.ui)
        init.configuration_device1.ui.setVisible(True)
        init.configuration_device1.ui.machine_name.setText(f"{init.configuration_device1.machine_name}+Configuration")
        Thread(target=init.configuration_device1.configuration_retrieve).start()
        init.init_machine1()
        window.stackedwidget_content_area.addWidget(init.machine1_user_page.ui)
        init.settings_page_init()        


    elif(name== "label_configure_machine2" ) :
        print("Clicked on configuration machine 2")
        window.stackedwidget_content_area.setCurrentWidget(init.configuration_device2.ui)
        init.configuration_device2.ui.setVisible(True)
        init.configuration_device2.ui.machine_name.setText(f"{init.configuration_device2.machine_name} Configuration")
        Thread(target=init.configuration_device2.configuration_retrieve).start()
        init.init_machine2()
        window.stackedwidget_content_area.addWidget(init.machine2_user_page.ui)
        init.settings_page_init()
    


#callback function for test connection
# def test_button_clicked(configuration) :
#     configuration.ui.status.setText("Please wait...")
#     configuration.ipaddress=configuration_device1.ui.ipaddress.text()
#     configuration.portnumber=int(configuration.ui.portnumber.text())
#     Thread(target=configuration.test_connection_clicked).start()

# def cancel_clicked() :
#     window.stackedwidget_content_area.setCurrentWidget(machine1_user_page.ui)

# def configuration_save_clicked(configuration) :
#     configuration.ui.status.setText("Saving configuration, please wait...")
#     Thread(target=configuration.save_clicked).start()
    

#User Page Save button click
def users_save_clicked(users_page) :
    users_page.ui.users_label.setText("Please wait ")
    Thread(target=users_page.save_user_payroll).start()



#Ui loads

# ui\claud main.ui
# window=loader.load("C:/Users/vaxso/Desktop/Attandance Management system/ui/main.ui")
window=loader.load(resource_path("ui/main.ui"))
#machine2_user_page=user_page(device_2).ui
window.stackedwidget_content_area.addWidget(init.machine2_user_page.ui)
window.stackedwidget_content_area.addWidget(init.machine1_user_page.ui)
window.stackedwidget_content_area.addWidget(init.configuration_device1.ui)
window.stackedwidget_content_area.addWidget(init.configuration_device2.ui)   
window.widget_sub_machine1.setVisible(False)
window.widget_sub_machine2.setVisible(False)


#clickfilter function to detect click on label and show user data in table
window.users_click=ClickFilter(user_btn_clicked)
window.attendance_click=ClickFilter(attandance_btn_clicked)
window.configuration_click=ClickFilter(configuration_btn_clicked)
window.settings_btn.clicked.connect(lambda :init.settings_page.ui.show()) 



# #Configuration page Buttons
# configuration_device1.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device1))
# configuration_device2.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device2))
# configuration_device1.ui.btn_cancel.clicked.connect(cancel_clicked)
# configuration_device2.ui.btn_cancel.clicked.connect(cancel_clicked)
# configuration_device1.ui.btn_save.clicked.connect(lambda: configuration_save_clicked(configuration_device1))
# configuration_device2.ui.btn_save.clicked.connect(lambda: configuration_save_clicked(configuration_device2))

#users page buttons
init.machine1_user_page.ui.Save_button.clicked.connect(lambda:users_save_clicked(init.machine1_user_page))


window.label_users_machine1.installEventFilter(window.users_click)
window.label_attandance_machine1.installEventFilter(window.attendance_click)
window.label_configure_machine1.installEventFilter(window.configuration_click)
window.label_users_machine2.installEventFilter(window.users_click)
window.label_attandance_machine2.installEventFilter(window.attendance_click)
window.label_configure_machine2.installEventFilter(window.configuration_click)

#Manually asigining device object to label for now, need to find better way to do this.
# window.label_attandance_machine1.device=init.device_1

window.widget_sub_machine1.setVisible(True)
window.widget_sub_machine2.setVisible(True)
window.progressBar.setVisible(False)

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
loading_page.close()
app.exec()

