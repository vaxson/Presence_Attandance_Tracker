from services.services import test_connection
from PySide6.QtCore import Qtimer


def test_connection_clicked(ipaddress,portnumber,callback) :
    result=test_connection(ipaddress=ipaddress,port=portnumber)
    print("test connection")
    callback(result["success"],result["status"])
   