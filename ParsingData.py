import pandas as pd

class ParsingData:
  def __init__(self) -> None:
    self.df = None
    self.data_male = None
    self.data_female = None
    self.data_more_age = None
    self.data_less_age = None
  

  def parse_file(self, file_path: str):
    '''
    Чтение и парсинг файла. Предобработка данных.

    Return:
      tuple(is_parse_ok: bool, message: str)
    '''

    try:
      self.df = pd.read_csv(file_path, encoding='cp1251', sep=',', quotechar="'")
      self.df.columns = ['Количество больничных дней', 'Возраст', 'Пол']
      self.df.replace('"', '', regex=True, inplace=True)
      self.df['Количество больничных дней'] = pd.to_numeric(self.df['Количество больничных дней'])
    except Exception as e:
      message = str(e)
      return False, message
    
    return True, 'Ok'
    
  
  def get_or_update_selections(self, age: int, work_days: int):
    '''
    Получения выборок для мужчин и женщин и выборок до младше и старше заданного возраста или их обновление для новых параметров.
    
    Args:
        age (граница возраста): int, 
        work_days (количество промущенных по болезни рабочих дней): int

    Return:
        is_ok (Корректные ли параметры): bool, 
        message (сообщение об ошибке): str
    '''

    self.df = self.df[self.df['Количество больничных дней'] > work_days]
    
    self.data_male = self.df[self.df['Пол'] == 'М']['Количество больничных дней']
    self.data_female = self.df[self.df['Пол'] == 'Ж']['Количество больничных дней']

    self.data_more_age = self.df[self.df['Возраст'] > age]['Количество больничных дней']
    self.data_less_age = self.df[self.df['Возраст'] <= age]['Количество больничных дней']

    if len(self.data_male) == 0 or len(self.data_male) == 0:
      return False, 'Неправильное условие на кол-во рабочих дней'
    if len(self.data_more_age) == 0 or len(self.data_less_age) == 0:
      return False, 'Неправильные условия на кол-во рабочих дней или границу возраста'
    return True, 'Ok'
