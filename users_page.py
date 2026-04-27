from PySide6.QtWidgets import QCheckBox, QLineEdit,QTableWidgetItem
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtGui import QDoubleValidator
from services.services import fetch_users_from_db,fetch_user_from_device,push_user_to_db


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
        self.ui=loader.load("ui/usersV2.ui")
        self.Modeluser=[]
        self.validator=QDoubleValidator(0.00, 1000000.00, 2)


    def display_users(self) :
        db_fetch=fetch_users_from_db(self.device)
        print(f"Inside display users function : device NAme={self.device.device_name}")
        if(db_fetch["success"]) :
            self.Modelusers=db_fetch["result"]
            self.ui.tableWidget.setRowCount(len(self.Modelusers))
            self.ui.tableWidget.setEnabled(True)
            print(f"parent :{self.ui.tableWidget.parent().isEnabled()} ")
            print(f"table enabled : {self.ui.tableWidget.isEnabled()}")
            row_position=0
            for user in self.Modelusers :
                print(f"At USer PAGE User name : {user.name}, UID : {user.uid}, password :{user.password}, isOtEnabled : {user.isOtEnabled}, salary : {user.salary} ")
                self.ui.tableWidget.setItem(row_position,0,QTableWidgetItem(str(user.uid)))
                self.ui.tableWidget.setItem(row_position,1,QTableWidgetItem(user.name))
                self.ui.tableWidget.setItem(row_position,2,QTableWidgetItem(user.password))
                ot_checkbox=QCheckBox()
                ot_checkbox.user_id=user.uid
                salary_input=QLineEdit()
                salary_input.user_id=user.uid
                salary_input.setPlaceholderText("Salary")
                salary_input.setValidator(self.validator)


                if(user.isOtEnabled) :
                    ot_checkbox.setChecked(True)
                else :
                    ot_checkbox.setChecked(False)
                self.ui.tableWidget.setCellWidget(row_position,3,ot_checkbox)
            
    
                if(user.salary) :
                    salary_input.setText(str(user.salary))
                else :
                    pass  
                self.ui.tableWidget.setCellWidget(row_position,4,salary_input) 
                row_position+=1
        elif(db_fetch["success"]==False) :
            self.status=db_fetch["result"]


    def save_user_payroll(self):
        print("At USP")
        for index,users in enumerate(self.Modelusers) :
            item_id=self.ui.tableWidget.item(index,0).text()
            item_isOtEnabled=self.ui.tableWidget.cellWidget(index,3).isChecked()
            item_salary=self.ui.tableWidget.cellWidget(index,4).text()
            #print(f"UID from table : {item_id} Salary from table : {item_salary} OT from table : {item_isOtEnabled}")
            if (item_salary) :
                item_salary=float(item_salary)
                users.salary=item_salary
    
            users.isOtEnabled=item_isOtEnabled
            print(f" Name : {users.name} OT : {users.isOtEnabled} Salary {users.salary}")
            push_user_to_db(self.Modelusers)
        print(" At save_user_payroll() Saved")


            
        


