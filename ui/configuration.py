from PySide6.QtUiTools import QUiLoader
from services.services import test_connection,configuration_retrieve_db,configuration_save,get_device_connection
from threading import Thread
import sys
from utils.helper import PyInstaller_helper
resource_path=PyInstaller_helper.resource_path



class ConfigurationDevice() :
    def __init__(self,id) :
        self.isonline=False
        self.machine_name=""
        self.id=id
        self.ipaddress=""
        self.portnumber=""
        self.ping_status=None
        loader=QUiLoader()
        self.ui=loader.load(resource_path("ui/configuration.ui"))
        self.configuration_retrieve()
        # self.device_object=None
        self.device_object=get_device_connection(ipaddress=self.ipaddress,port_number=self.portnumber,device_name=self.machine_name)
        Thread(target=self.checkstatus).start()
        self.ui.btn_test_connection.clicked.connect(self.test_connection_clicked)
        self.ui.btn_save.clicked.connect(self.save_clicked)
        self.ui.btn_cancel.clicked.connect(self.close_clicked)

        
    def checkstatus(self) :
        # test_conncection()    FROM SERVICE MODULE
        status=test_connection(ipaddress=self.ipaddress,port_number=self.portnumber)["success"]
        # If Device got disconnected while sofware is running and when connecting the device back will cause dice object to be of sync.
        # This line checks whether the isOnline and the status variable are diffrent, if so a connection change is expected and new device object 
        # is restored.
        if(status==True and self.isonline==False) :
            self.device_object=get_device_connection(ipaddress=self.ipaddress,port_number=self.portnumber,device_name=self.machine_name)
            print(f"CON:32| device connection object restored")
        self.isonline=status
        return self.isonline
        
        
    def test_connection_clicked(self) :
        self.ui.status.setText("Testing connection...")
        Thread(target=self.thread_test_connection).start()
        # print(f"Device {self.machine_name} is Offline")


    def thread_test_connection(self) :
        self.ui.status.setText("")
        test_status=test_connection(ipaddress=self.ui.ipaddress.text(),port_number=int(self.ui.portnumber.text()))
        print(f"IP :{self.ui.ipaddress.text()} | PORT : {self.ui.portnumber.text()}")
        if(test_status["success"]) :
            self.ui.status.setText("Connection successful.")
        else :
            self.ui.status.setText(f"Connection failed: {test_status['status']}")
    
    def configuration_retrieve(self) :
        # self.ui.setVisible(True)
        retrieved=configuration_retrieve_db(configuration_id=int(self.id))
        if(retrieved["success"]) :
            self.ui.devicename.setText(retrieved["configuration"][1])
            self.machine_name=retrieved["configuration"][1]
            self.ui.ipaddress.setText(retrieved["configuration"][2])
            self.ipaddress=retrieved["configuration"][2]
            self.ui.portnumber.setText(str(retrieved["configuration"][3]))
            self.portnumber=retrieved["configuration"][3]
            self.ui.machine_name.setText(retrieved["configuration"][1])
        else:
        
            self.ui.status.setText(retrieved["configuration"])



    def save_clicked(self):
        Thread(target=self.thread_save_clicked).start()
        self.ui.status.setText("Saving Please Wait...")
        

    def thread_save_clicked(self ):
        self.ui.status.setText("")
        save_status=configuration_save(self.id,self.ui.devicename.text(),self.ui.ipaddress.text(),int(self.ui.portnumber.text()))
        self.configuration_retrieve()
        self.device_object=get_device_connection(ipaddress=self.ipaddress,port_number=self.portnumber,device_name=self.machine_name)  
        self.ui.status.setText(save_status['status'])
        print(f"Save Clicked parent :{self.ui.parent().parent()}")

    def close_clicked(self) :
      self.ui.setVisible(False)

        
   

