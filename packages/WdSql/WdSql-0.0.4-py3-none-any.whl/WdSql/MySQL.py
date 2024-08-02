import traceback

from mysql.connector import connect

from .import utils
from .error import Database_Error
from .objects import Database_Result

class MySQl:
  def __init__(self):
    pass

  def select(self, key: dict, query:str, params:list = None)->Database_Result:
    data:dict = {}
    conexion:connect = None
    cursor:connect.cursor = None
    result:Database_Result = None
    try:
      conexion = connect(**key)
      cursor = conexion.cursor() 
      data['operation']=query
      if params: data['params']=params
      cursor.execute(**data)
      tabla = utils.format_result(cursor.fetchall(), cursor.description)
      result = Database_Result(
        row_count=cursor.rowcount,
        last_id=cursor.lastrowid,
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
      
  def execute(self, key: dict, query:str, params:list = None)->Database_Result:
    data:dict = {}
    conexion:connect = None
    cursor:connect.cursor = None
    result:Database_Result = None
    try:
      conexion = connect(**key)
      cursor = conexion.cursor()
      data['operation']=query
      if params: data['params']=params
      cursor.execute(**data)
      conexion.commit()
      result = Database_Result(
        row_count=cursor.rowcount,
        last_id=cursor.lastrowid,
        data=[]
        )
      cursor.close()
      conexion.close()
      return result
    except Exception as e:
      if cursor: cursor.close()
      if conexion: conexion.close()
      raise Database_Error(
        message='Error in execute',
        error_information=traceback.format_exc(),
        status_code=502
      )
    