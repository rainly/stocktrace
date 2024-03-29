'''
Created on 2012-10-9

@author: Simon
'''
import win32service
import win32serviceutil
import win32api
import win32con
import win32event
import win32evtlogutil
import os
from stocktrace.cron.monitor import Monitor

monitor = Monitor()

class StockTraceService(win32serviceutil.ServiceFramework):
   
   _svc_name_ = "StockTrace"
   _svc_display_name_ = "stock price polling service"
   _svc_description_ = "polling real time stock price from sina periodically"
         
   def __init__(self, args):
           win32serviceutil.ServiceFramework.__init__(self, args)
           self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)           

   def SvcStop(self):
#           from stocktrace.cron.realtimemonitorschedule import stopMonitor
#           stopMonitor()  
           monitor.stop()
           self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
           win32event.SetEvent(self.hWaitStop)                    
         
   def SvcDoRun(self):
      import servicemanager      
      servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,servicemanager.PYS_SERVICE_STARTED,(self._svc_name_, '')) 
      
      self.timeout = 3000
#      from stocktrace.cron.realtimemonitorschedule import startMonitor
#      startMonitor()    
      monitor.start()       

    
      while 1:
         # Wait for service stop signal, if I timeout, loop again
         rc = win32event.WaitForSingleObject(self.hWaitStop, self.timeout)
         # Check to see if self.hWaitStop happened
         if rc == win32event.WAIT_OBJECT_0:
            # Stop signal encountered
            servicemanager.LogInfoMsg("StockMonitorService - STOPPED")
            break
         else:
            servicemanager.LogInfoMsg("StockMonitorService - is alive and well")   
               
      
def ctrlHandler(ctrlType):
   return True
                  
if __name__ == '__main__':   
   win32api.SetConsoleCtrlHandler(ctrlHandler, True)   
   win32serviceutil.HandleCommandLine(StockTraceService)