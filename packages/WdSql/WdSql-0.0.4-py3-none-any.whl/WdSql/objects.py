class Database_Result:
  def __init__(
      self, 
      row_count:int,
      last_id:int,
      data:list
      ):
    self.row_count=row_count
    self.last_id=last_id
    self.data = data