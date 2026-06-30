from threading import Thread

from PySide6.QtWidgets import QCheckBox, QLineEdit,QTableWidgetItem
from PySide6.QtUiTools import QUiLoader 
from PySide6.QtGui import QDoubleValidator
from services.services import fetch_users_from_db,push_software_user_to_db
from utils.helper import PyInstaller_helper
resource_path=PyInstaller_helper.resource_path

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
        self.ui=loader.load(resource_path("ui/users.ui"))
        self.Modeluser=[]
        self.validator=QDoubleValidator(0.00, 1000000.00, 2)
        self.ui.Save_button.clicked.connect(self.save_user_payroll)


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
                ot_checkbox.setStyleSheet("""
                    QCheckBox {
                                spacing: 8px;
                                font-size: 13px;
                                color: #111827;
                                background-color: transparent;
                                alignment: center;
                            }

                            QCheckBox::indicator {
                                width: 18px;
                                height: 18px;
                                border-radius: 18px;
                                border: 2px solid #CBD5E1;
                                background-color: white;
                            }

                            QCheckBox::indicator:hover {
                                border: 2px solid #4F46E5;
                            }


                            QCheckBox::indicator:checked {
                                background-color:#4F46E5;
                                border: 2px solid #4F46E5;
                            }
                                            """)    
                
                ot_checkbox.user_id=user.uid

                salary_input = QLineEdit()
                salary_input.setStyleSheet("""
                    QLineEdit {
                        background-color: transparent;
                        font-size: 12px;
                        font-weight: bold;
                        color: #e2e8f0;
                        border: 0px solid #3a3a55;
                        border-radius: 1px;
                        padding: 0px;
                    }
                    QLineEdit:focus {
                        border: 0px solid #4da3ff;
                        background-color: #252538;
                    }
                    QLineEdit:hover {
                        border: 0px solid #4a4a6a;
                    }
                """)
                salary_input.user_id = user.uid
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
        self.ui.users_label.setText("Saving Please Wait....")
        Thread(target=self.threaded_save_user_payroll).start()
        

    def threaded_save_user_payroll(self) :
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
            push_software_user_to_db(self.Modelusers)
        print(" At save_user_payroll() Saved")
        self.ui.users_label.setText("Saved Successfully")

        

            
        


