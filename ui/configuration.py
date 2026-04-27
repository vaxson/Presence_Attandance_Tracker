from PySide6.QtUiTools import QUiLoader
from services.services import test_connection,configuration_retrieve_db,configuration_save


class ConfigurationDevice :
    def __init__(self,id) :
        self.machine_name=None
        self.id=id
        self.ipaddress=None
        self.portnumber=None
        self.ping_status=None
        loader=QUiLoader()
        self.ui=loader.load("ui/configuration.ui")

    def test_connection_clicked(self) :
        result=test_connection(ipaddress=self.ipaddress,port_number=self.portnumber)
        print("test connection")
        self.ui.ping_status.setText(result['status'])
    
    def configuration_retrieve(self) :
        retrieved=configuration_retrieve_db(configuration_id=int(self.id))
        if(retrieved["success"]) :
            self.ui.devicename.setText(retrieved["configuration"][1])
            self.ui.ipaddress.setText(retrieved["configuration"][2])
            self.ui.portnumber.setText(str(retrieved["configuration"][3]))
            self.ui.machine_name.setText(retrieved["configuration"][1])
        else:
        
            self.ui.status.setText(retrieved["configuration"])

    def save_clicked(self):
        save_status=configuration_save(self.id,self.ui.devicename.text(),self.ui.ipaddress.text(),int(self.ui.portnumber.text()))
        self.ui.ping_status.setText(save_status['status'])

        
   

