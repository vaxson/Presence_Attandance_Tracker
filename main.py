from mimetypes import init

from services.services import *
from PySide6.QtWidgets import QApplication,QTableWidgetItem,QLabel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QThread,Signal
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


# Initialization object


# Initialization workerclass
class WorkerInitialization(QThread) :
    print("MN :57 AT Worker")
    progress=Signal(int,str)
    finished=Signal(object)
    
    def run(self) :
        print("Worker thread started")
        self.progress.emit(20,"Initializing objects....")
        init=initialization()
        print("MN : 63 Initialization complete")
        self.progress.emit(50,"Initialization complete")
        print("MN : 65 Checking device status")
        init.configuration_device1.checkstatus()
        self.progress.emit(80,"Checking device_1 status....")
        init.configuration_device2.checkstatus()
        self.progress.emit(100,"Checking device_2 status....")
        print("MN : 70 Device status check complete")
        self.finished.emit(init)



    
# Loading Page
class LoadingPage() :
    def __init__(self) :
        self.loading_page=loader.load(resource_path("ui/loading_page.ui"))
        self.loading_page.show()
        self.worker=WorkerInitialization()
        self.worker.progress.connect(self.on_progress)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()
        print("Loading")

    def on_progress(self,value,message) :
        print(f"progress :({value}%) : {message}")
        self.loading_page.progressBar.setValue(value)
        self.loading_page.lab_process.setText(message)
    def on_finished(self,init_object) :
        self.loading_page.progressBar.setValue(100)
        self.loading_page.lab_process.setText("Initialization finished.")
        self.loading_page.close() 
        self.initialize=init_object
        print("Showing main window")
        show_main()
        

class MainWindow() :
    def __init__(self,initialization_object) :
        self.init=initialization_object
        self.window=loader.load(resource_path("ui/main.ui"))
        self.window.stackedwidget_content_area.addWidget(self.init.machine2_user_page.ui)
        self.window.stackedwidget_content_area.addWidget(self.init.machine1_user_page.ui)
        self.window.stackedwidget_content_area.addWidget(self.init.configuration_device1.ui)
        self.window.stackedwidget_content_area.addWidget(self.init.configuration_device2.ui)   
        self.window.widget_sub_machine1.setVisible(False)
        self.window.widget_sub_machine2.setVisible(False)

        #clickfilter function to detect click on label and show user data in table
        self.window.users_click=ClickFilter(self.user_btn_clicked)
        self.window.attendance_click=ClickFilter(self.attandance_btn_clicked)
        self.window.configuration_click=ClickFilter(self.configuration_btn_clicked)
        self.window.settings_btn.clicked.connect(lambda :self.init.settings_page.ui.show())

        # #Configuration page Buttons
        # configuration_device1.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device1))
        # configuration_device2.ui.btn_test_connection.clicked.connect(lambda :test_button_clicked(configuration_device2))
        # configuration_device1.ui.btn_cancel.clicked.connect(cancel_clicked)
        # configuration_device2.ui.btn_cancel.clicked.connect(cancel_clicked)
        # configuration_device1.ui.btn_save.clicked.connect(lambda: configuration_save_clicked(configuration_device1))
        # configuration_device2.ui.btn_save.clicked.connect(lambda: configuration_save_clicked(configuration_device2))

        #users page buttons
        self.init.machine1_user_page.ui.Save_button.clicked.connect(lambda: self.users_save_clicked(self.init.machine1_user_page))


        self.window.label_users_machine1.installEventFilter(self.window.users_click)
        self.window.label_attandance_machine1.installEventFilter(self.window.attendance_click)
        self.window.label_configure_machine1.installEventFilter(self.window.configuration_click)
        self.window.label_users_machine2.installEventFilter(self.window.users_click)
        self.window.label_attandance_machine2.installEventFilter(self.window.attendance_click)
        self.window.label_configure_machine2.installEventFilter(self.window.configuration_click)

        #Manually asigining device object to label for now, need to find better way to do this.
        # window.label_attandance_machine1.device=init.device_1

        self.window.widget_sub_machine1.setVisible(True)
        self.window.widget_sub_machine2.setVisible(True)
        self.window.progressBar.setVisible(False)
        #self.window.rbtn_machine1.toggled.connect(showhide_machineSubbuttons)
        print("Main window loaded")
        self.window.show()

    def check_stauts(self) :
        Thread(target=self.init.configuration_device1.checkstatus).start()
        Thread(target=self.init.configuration_device2.checkstatus).start()

    
    def syncMachine(self, device, attendance_page) :
        print("00%")
        self.window.progressBar.setVisible(True)
        try :
            fetch_user_from_device(device)
        except Exception as e :
            return e
        self.window.progressBar.setValue(50)
        print("50%")
        if(attendance_page) :
            try :
                attendance_page.sync_attendance(device)
            except Exception as e :
                return e
        self.window.progressBar.setValue(100)
        print("100%")
        self.window.progressBar.setVisible(False)
        return True 
    

    def user_btn_clicked(self, obj) :
        self.check_stauts()
        #drop_database_table(device_1,1)
        name=obj.objectName()
        print(f"Object name: {name}")
        # Selection for machine 1
        if(name=="label_users_machine1") :
            print("Clicked on user machine 1")
            if(self.init.configuration_device1.isonline) :
                self.init.machine1_user_page.ui.users_label.setText("Device Online")
                self.syncMachine(self.init.configuration_device1.device_object,None)
            else :
                self.init.machine1_user_page.ui.users_label.setText("Device Offline")
            self.window.stackedwidget_content_area.setCurrentWidget(self.init.machine1_user_page.ui)
            self.init.machine1_user_page.display_users()

        #Selection for machine 2 
        elif name == "label_users_machine2":
            print("Clicked on user machine 2")
            #   Display the online status of the device in the user page label
            if(self.init.configuration_device2.isonline) :
                self.init.machine2_user_page.ui.users_label.setText("Device Online")
                self.syncMachine(self.init.configuration_device2.device_object,None)
            else :
                self.init.machine2_user_page.ui.users_label.setText("Device Offline")
            self.window.stackedwidget_content_area.setCurrentWidget(self.init.machine2_user_page.ui)
            self.init.machine2_user_page.display_users()
        print("Exited")
        
    
    def attandance_btn_clicked(self, obj) :
        self.check_stauts()
        self.window.attendance_page=Attendance_page()
        attendance_page=self.window.attendance_page
        name=obj.objectName()
        if(name== "label_attandance_machine1") :
            print(f"Clicked on attendance machine 1") 
            if(self.init.configuration_device1
            
            .isonline) :
                # syncMachine(init.device_2,None)
                self.syncMachine(self.init.configuration_device1.device_object,attendance_page)
        
            self.init.date_selection.ui.exec()
            start_date=self.init.date_selection.start_date
            end_date=self.init.date_selection.end_date
            if(start_date !=None and end_date !=None) :
                attendance_page.get_attendance(self.init.configuration_device1.device_object,self.init.settings_page,start_date,end_date)
                attendance_page.ui.show()
            else :
                print("invalid date selection")
            

        elif(name == "label_attandance_machine2") :
            print("Clicked on attendance machine 2")
            if(self.init.configuration_device2.isonline) :
                self.syncMachine(self.init.configuration_device2.device_object,attendance_page)

            self.init.date_selection.ui.exec()
            start_date=self.init.date_selection.start_date
            end_date=self.init.date_selection.end_date
            if(start_date !=None and end_date !=None) :
                attendance_page.get_attendance(self.init.configuration_device2.device_object,self.init.settings_page,start_date,end_date)
                attendance_page.ui.show()
            else :
                print("invalid date selection")
        # attendance_page=Attendance_page()

    
    def configuration_btn_clicked(self, obj) :
        init=self.init
        self.check_stauts()
        name=obj.objectName()
        if(name== "label_configure_machine1") :
            print("Clicked on configuration machine 1")
            self.window.stackedwidget_content_area.setCurrentWidget(self.init.configuration_device1.ui)
            init.configuration_device1.ui.setVisible(True)
            init.configuration_device1.ui.machine_name.setText(f"{init.configuration_device1.machine_name}+Configuration")
            Thread(target=init.configuration_device1.configuration_retrieve).start()
            init.init_machine1()
            self.window.stackedwidget_content_area.addWidget(init.machine1_user_page.ui)
            init.settings_page_init()        


        elif(name== "label_configure_machine2" ) :
            print("Clicked on configuration machine 2")
            self.window.stackedwidget_content_area.setCurrentWidget(init.configuration_device2.ui)
            init.configuration_device2.ui.setVisible(True)
            init.configuration_device2.ui.machine_name.setText(f"{init.configuration_device2.machine_name} Configuration")
            Thread(target=init.configuration_device2.configuration_retrieve).start()
            init.init_machine2()
            self.window.stackedwidget_content_area.addWidget(init.machine2_user_page.ui)
            init.settings_page_init()

        
    #User Page Save button click
    def users_save_clicked(self, users_page) :
        users_page.ui.users_label.setText("Please wait ")
        Thread(target=users_page.save_user_payroll).start()
        


            
    



loading_page=LoadingPage()



def show_main() :
    window=MainWindow(initialization_object=loading_page.initialize)
    
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

# '''Callback Functions'''
# '''
# #callback return the status of test connection and update the label in configuration page
# def test_connection_status(status, message,configure_ui_id) :
#     if(configure_ui_id==1) :
#         configuration_device1.ui.status.setText(message)
#     elif(configure_ui_id==2) :
#         configuration_device2.ui.status.setText(message)
# '''

    

# check_stauts()

        
        
#callback for user button machine 1 and 2


#callback for attendance button machine 1 and 2  

    
#callback for configuration button machine 1 and 2



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
    





#Ui loads

# ui\claud main.ui
# window=loader.load("C:/Users/vaxso/Desktop/Attandance Management system/ui/main.ui")





# '''
# table = machine1_user_page.tableWidget
# table.horizontalHeader().setVisible(True)
# table.horizontalHeader().setFixedHeight(50)
# table.setColumnCount(3)
# table.setHorizontalHeaderLabels(["Date","Day","Status"])
# table.setRowCount(len(user_data))


# for user, row in enumerate(user_data):
    
#     table.setItem(user, 0, QTableWidgetItem(str(row[0])))
#     table.setItem(user, 1, QTableWidgetItem(str(row[1])))
#     table.setItem(user, 2, QTableWidgetItem(str(row[2])))

# '''


app.exec()

