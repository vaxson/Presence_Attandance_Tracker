from PySide6.QtCore import QObject, QEvent

class ClickFilter(QObject):
    def __init__(self, callback):
        super().__init__()
        self.callback=callback

    def eventFilter(self,obj,event):
        if event.type()==QEvent.MouseButtonPress:
           self.callback(obj)
           return True
        else:
            return False