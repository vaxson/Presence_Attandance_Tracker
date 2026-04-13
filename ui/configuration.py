from PySide6.QtWidgets import QTableWidgetItem,QLabel,QFrame
from PySide6.QtUiTools import QUiLoader
from services.services import test_connection
from PySide6.QtCore import QTimer

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

    def save_clicked(self):
        pass 

        
   

