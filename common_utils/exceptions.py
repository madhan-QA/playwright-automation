class AutomationError(Exception):
  
    def __init__(self, message: str, error_code: str = None):
        
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class LoginError(AutomationError):
   
    def __init__(self, message: str, error_code: str = "LOGIN_FAILED"):
       
        super().__init__(message, error_code)

class NavigationError(AutomationError):
   
    def __init__(self, message: str, error_code: str = "NAVIGATION_FAILED"):
       
        super().__init__(message, error_code)

class DownloadError(AutomationError):
    
    def __init__(self, message: str, error_code: str = "DOWNLOAD_FAILED"):
        
        super().__init__(message, error_code)

class CalculationError(AutomationError):
    def __init__(self, message:str ,error_code: str ="CALCULATION_FALIED"):
        super().__init__(message, error_code)