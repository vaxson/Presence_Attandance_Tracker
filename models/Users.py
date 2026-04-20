class Users :
    def __init__(self,uid,name,password,device_name):
        self.device_name=device_name
        self.uid=uid
        self.name=name
        self.password=password
        self.salary=0
        self.isOtEnabled=False

    def db_push(self) :
        pass