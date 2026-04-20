from PySide6.QtWidgets import QCheckBox, QLineEdit, QTableWidgetItem,QLabel,QFrame
from PySide6.QtUiTools import QUiLoader
from PySide6.QtCore import QTimer
from services.services import fetch_users_from_db,fetch_user_from_device

'''
    * Note The user_page needs device object as the parameter 
      to fetch the users from the device and display it in the table widget.
    * It is not looking for anything else but the ZK object which is created in the main.py file 
      and passed to the user_page class.
'''

class user_page() :
    def __init__(self,device) :
        self.device=device
        loader=QUiLoader()
        self.ui=loader.load("ui/users.ui")


    def display_users(self) :
        device_fetch=fetch_user_from_device(self.device)
        db_fetch=fetch_users_from_db(self.device)

        if(device_fetch["success"]) :
            users=device_fetch["result"]
            self.ui.tableWidget.setRowCount(len(users))
            for user in users :
                row_position=user.uid
                self.ui.tableWidget.setItem(row_position,0,QTableWidgetItem(user.uid))
                self.ui.tableWidget.setItem(row_position,1,QTableWidgetItem(user.name))
                self.ui.tableWidget.setItem(row_position,2,QTableWidgetItem(user.password))
                if(db_fetch.isOtEnabled) :
                    ot_checkbox=QCheckBox()
                    ot_checkbox.setChecked(True)
                    ot_checkbox.user_id=user.uid
                    self.ui.tableWidget.setCellWidget(row_position,3,ot_checkbox)
                else :
                    self.ui.tableWidget.setCellWidget(row_position,3,QCheckBox())
                #self.ui.tableWidget.setItem(row_position,3,QTableWidgetItem(str(user.isOtEnabled)))
                if(user.salary>0) :
                    salary_input=QLineEdit()
                    salary_input.setText(str(user.salary))
                    salary_input.user_id=user.uid
                else :
                    self.ui.tableWidget.setCellWidget(row_position,4,salary_input.placeholderText("Enter Salary")) 

        elif(device_fetch["success"]==False) :
            self.status=device_fetch["result"]


