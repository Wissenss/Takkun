from datetime import datetime


class DBUtils:

  TIMESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S" 
  
  def __init__(self):
     pass
  
  def parse_datetime_str(datetime_str : str) -> datetime:
    if datetime_str == None:
      return None 
    
    return datetime.strptime(datetime_str, DBUtils.TIMESTAMP_FORMAT)     
  
  def format_db_date(date : datetime) -> str:
    if date == None:
        return None
    
    return date.strftime(DBUtils.TIMESTAMP_FORMAT)