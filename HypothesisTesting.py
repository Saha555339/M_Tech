from scipy import stats
import pandas as pd

class HypothesisTesting:
  
  @staticmethod
  def __is_corr(df1, df2) -> tuple:
    '''
    Проверка коррелируемости данных.
    
    Метод: Коэффициент корреляции Спирмена.

    Return:
      tuple(corr, p_value)
    '''

    min_len = min(len(df1), len(df2))
    corr, p_value = stats.spearmanr(df1.sample(min_len), df2.sample(min_len))

    return corr, p_value
  

  @staticmethod
  def __is_normal(data) -> tuple:
    '''
    Проверка данных на нормальность.
    
    Метод: Тест Шапиро-Уилка.

    Return:
      tuple(corr, p_value)
    '''

    statistic, p_value = stats.shapiro(data)
    return statistic, p_value
  
  @staticmethod
  def __mannwhitneyu_test(df1, df2) -> tuple:
    '''
    Проверка гипотезы о том, что среднее первой выборки больше, чем среднее второй.
    
    Условия: Некоррелированные выборки, неизвестного распределения.
    
    Метод: U-критерий Манна - Уитни.

    Return:
      tuple(corr, p_value)
    '''

    statistic, p_value = stats.mannwhitneyu(df1, df2, alternative='greater')
    return statistic, p_value
  
  @staticmethod
  def __wilcoxon_test(df1, df2) -> tuple:
    '''
    Проверка гипотезы о том, что среднее первой выборки больше, чем среднее второй.
    
    Метод: Критерий Уилкоксона.

    Return:
      tuple(corr, p_value)
    '''

    statistic, p_value = stats.wilcoxon(df1, df2, alternative='greater')
    return statistic, p_value
  
  @staticmethod
  def __ttest_corr(df1, df2) -> tuple:
    '''
    Проверка гипотезы о том, что среднее первой выборки больше, чем среднее второй.
    
    Условия: Выборка из нормального распределения.
    
    Метод: T-критерий Стьюдента.

    Return:
      tuple(corr, p_value)
    '''

    statistic, p_value = stats.ttest_rel(df1, df2, alternative='greater')
    return statistic, p_value
  
  @staticmethod
  def __ttest_not_corr(df1, df2) -> tuple:
    '''
    Проверка гипотезы о том, что среднее первой выборки больше, чем среднее второй.
    
    Условия: Некоррелированные выборки, нормального распределения.
    
    Метод: T-критерий Стьюдента.

    Return:
      tuple(corr, p_value)
    '''

    statistic, p_value = stats.ttest(df1, df2, alternative='greater')
    return statistic, p_value


  def testing_the_hypothesis_of_avg(self, df1, df2) -> tuple:
    '''
    Проверка гипотезы о том, что среднее первой выборки больше, чем среднее второй.
    (В качестве дополнительных проверок: тест на наормальность, на коррелируемость)

    Return:
      is_first_avg_more_then_second: bool, 
      tests: list
    
    tests: df с полями | Название теста | Statistics/Corr | p_value |
    '''

    tests = []

    statistics_norm, p_value_norm = self.__is_normal(pd.concat([df1,df2]))
    test1 = {'Название теста': 'Тест Шапиро-Уилка', 'Statistics/Corr': statistics_norm,
            'p_value': p_value_norm}
    tests.append(test1)

    corr, p_value_corr = self.__is_corr(df1, df2)
    test2 = {'Название теста': 'Спирмен', 'Statistics/Corr': corr, 
            'p_value': p_value_corr}
    tests.append(test2)



    ## Проверка гипотезы о среднем происзодит следующим образом.
    # Сначала проводится тест Шапиро-Уилка на нормальность.
    # И тест Спирмена на коррелируемость значений.
    # Если данные распределены нормально, то используется T-критерий Стьюдента (для коррелируемых и нет выборо соответственно)
    # Если данные не распределены нормально, то используются непараметрический методы.
    # U-критерий Манна-Уитниа для некоррелируемых выборок и критерий Уилкоксона для коррелируемых.

    if p_value_norm < .05:
      if corr > 0.7 and p_value_corr > .05:
        statistic_avg, p_value_avg = self.__wilcoxon_test(df1, df2)
        test = {'Название теста': 'Критерий Уилкоксона', 'Statistics/Corr': statistic_avg,
            'p_value': p_value_avg}
        tests.append(test)
        if p_value_avg < .05:
          return True, tests
        else:
          return False, tests

      else:
        statistic_avg, p_value_avg = self.__mannwhitneyu_test(df1, df2)
        test = {'Название теста': 'U-критерий Манна - Уитниа', 'Statistics/Corr': statistic_avg,
            'p_value': p_value_avg}
        tests.append(test)
        if p_value_avg < .05:
          return True, tests
        else:
          return False, tests

    else:
      if corr > 0.7 and p_value_corr > .05:
        statistic_avg, p_value_avg = self.__ttest_corr(df1, df2)
        test = {'Название теста': 'T-критерий Стьюдента', 'Statistics/Corr': statistic_avg,
            'p_value': p_value_avg}
        tests.append(test)
        if p_value_avg < .05:
          return True, tests
        else:
          return False, tests

      else:
        statistic_avg, p_value_avg = self.__ttest_not_corr(df1, df2)
        test = {'Название теста': 'T-критерий Стьюдента', 'Statistics/Corr': statistic_avg,
            'p_value': p_value_avg}
        tests.append(test)
        if p_value_avg < .05:
          return True, tests
        else:
          return False, tests

