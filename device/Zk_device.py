from zk import ZK #pyzk library

# All methords of this class starts at capital letter to avoid confusion with the pyzk library methords which starts with small letter
class Zk_device :
    def __init__(self,ip,port,timeout,device_name):
        self.device_name=device_name
        self.ip_address=ip
        self.port=port
        self.timeout=timeout
        self.connection=None

    def Connect(self):
        zk=ZK(self.ip_address,self.port,self.timeout)
        try:
            print("Connecting to device......")
            self.connection=zk.connect()
            print("Disabling device......")
            self.connection.disable_device()
            return { "success": True, "object": self.connection }

        except Exception as e:
            print(f"Process failed : {e}")
            return { "success": False, "object": str(e) }



    def Disconnect(self):
        if self.connection:
            self.connection.enable_device()
            self.connection.disconnect()


    def Fetch_users(self):
        try :
            users=self.connection.get_users()
            return {"success":True,"result":users}
        except Exception as e :
            print(f"Error Occured : {e}")
            return {"success":False,"result":str(e)}

    
    def Fetch_attendance(self):
        try :
            attendance=self.connection.get_attendance()          
            return {"success":True,"result":attendance}
        except Exception as e :
            print(f"Error Occured : {e}")
            return {"success":False,"result":str(e)}

            