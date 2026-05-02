from PySide6.QtUiTools import QUiLoader
from services.services import test_connection,configuration_retrieve_db,configuration_save,get_device_connection


class ConfigurationDevice :
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
        self.device_object=get_device_connection(ipaddress=self.ipaddress,port_number=self.portnumber,device_name=self.machine_name)
        self.checkstatus()

    def checkstatus(self) :
        self.isonline=test_connection(ipaddress=self.ipaddress,port_number=self.portnumber)["success"]
        return self.isonline
        
        
    def test_connection_clicked(self) :
        result=test_connection(ipaddress=self.ipaddress,port_number=self.portnumber)
        print("test connection")
        self.isonline=result["success"]
        self.ui.ping_status.setText(result['status'])
    
    def configuration_retrieve(self) :
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
        self.ui.ping_status.setText(save_status['status'])

        
   

