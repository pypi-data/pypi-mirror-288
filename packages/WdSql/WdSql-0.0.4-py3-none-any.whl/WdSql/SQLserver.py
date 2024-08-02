import traceback

from pyodbc import connect

from .import utils
from .error import Database_Error
from .objects import Database_Result

class SQLServer:
  def __init__(self):
    pass

  def select(self, key:str, query:str, params:list=None):
    conexion:connect = None
    cursor:connect.cursor = None
    result:Database_Result = None
    try:      
      conexion = connect(key)
      cursor = conexion.cursor()
      if params:
        query = query.replace('%s','?')        
        cursor.execute(query, params)
      else:
        cursor.execute(query)
      tabla = utils.format_result(cursor.fetchall(), cursor.description)    
      result = Database_Result(
        row_count=len(tabla),
        last_id=-1,
        data=tabla
      )
      cursor.close()
      conexion.close()
      return result
    except Exception as e:
      if cursor: cursor.close()
      if conexion: conexion.close()
      raise Database_Error(
        message='Error in consult',
        error_information=traceback.format_exc(),
        status_code=502
      )