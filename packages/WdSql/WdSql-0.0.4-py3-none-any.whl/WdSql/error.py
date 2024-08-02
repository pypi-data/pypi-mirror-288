from wellog import loggen
class Database_Error(Exception):
  '''Database related errors. The error is automatically captured in the log file'''
  def __init__(self, 
               message, 
               error_information=None, 
               status_code=502):
    self._msg = message
    self._code = status_code
    if not error_information:
      loggen.error(f'({self._msg}) => [{error_information}]')

  def __str__(self):
        return self._msg
  
  @property
  def message(self):
     '''Controlled message'''
     return self._msg
  
  @property
  def status_code(self):
     '''Assigned status code'''
     return self._code
  
  @property
  def response(self)->dict:
     '''Web response, `result`, `message` and `data` are included'''
     return {
        "result":False,
        "message":self.message,
        "data":[]
     }