from PySide6.QtUiTools import QUiLoader
from services.services import test_connection,configuration_retrieve_db,configuration_save,get_device_connection
from threading import Thread


class ConfigurationDevice() :
    def __init__(self,id) :
        self.isonline=False
        self.machine_name=""
        self.id=id
        self.ipaddress=""
        self.portnumber=""
        self.ping_status=None
        loader=QUiLoader()
        self.ui=loader.load("ui/configuration.ui")
        self.configuration_retrieve()
        # /self.device_object=None
        self.device_object=get_device_connection(ipaddress=self.ipaddress,port_number=self.portnumber,device_name=self.machine_name)
        self.checkstatus()
        self.ui.btn_test_connection.clicked.connect(self.test_connection_clicked)
        self.ui.btn_save.clicked.connect(self.save_clicked)
        self.ui.btn_cancel.clicked.connect(self.close_clicked)

        
    def checkstatus(self) :
        self.isonline=test_connection(ipaddress=self.ipaddress,port_number=self.portnumber)["success"]
        return self.isonline
        
        
    def test_connection_clicked(self) :
        self.ui.status.setText("Testing connection...")
        Thread(target=self.thread_test_connection).start()

    def thread_test_connection(self) :
        test_status=test_connection(ipaddress=self.ui.ipaddress.text(),port_number=int(self.ui.portnumber.text()))
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
        save_status=configuration_save(self.id,self.ui.devicename.text(),self.ui.ipaddress.text(),int(self.ui.portnumber.text()))
        self.ui.status.setText(save_status['status'])

    def close_clicked(self) :
      self.ui.setVisible(False)

        
   

