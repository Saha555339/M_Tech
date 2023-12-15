from ParsingData import ParsingData
from HypothesisTesting import HypothesisTesting
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd


def upload_data_file_and_params():
    file_path_upload = st.file_uploader("Выберите CSV файл", type=["csv"], )
    age = st.number_input('Введите границу возраста, по которому будет разделение', value=35)
    work_days = st.number_input('Введите количество пропущенных рабочих дней', value=2)

    return file_path_upload if file_path_upload is not None else 'data.csv', age, work_days


def testing_hypothesis_and_draw_results(age, work_days, H0_sex, H0_age, tests_sex, tests_age):

    st.subheader('Мужчины и женщины')
    st.write(f'Гипотеза о том, что мужчины пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще женщин: {H0_sex}')
    st.write(pd.DataFrame(tests_sex))
    st.subheader('Молодые и постарше')
    st.write(f'Гипотеза о том, что работники старше {age} лет пропускают в течение года более {work_days} рабочих дней по болезни значимо чаще своих более молодых коллег: {H0_age}')
    st.write(pd.DataFrame(tests_age))


def draw_histograms(data_plot: list, age: int):
    plot_titles = ['Male', 'Female', f'More {age}', f'Less {age}']

    binwidth = st.slider('Выберите ширину бина', min_value=1, max_value=20, value=6)

    # Создание гистограмм
    for i, data in enumerate(data_plot):
        st.subheader(f'Histogram {plot_titles[i]}')
        plt.hist(data, bins=binwidth, color='blue', edgecolor='black')
        plt.xlabel('Дни')
        plt.ylabel('Количество человек')
        st.pyplot()


if __name__ == "__main__":

    st.set_option('deprecation.showPyplotGlobalUse', False)
    st.title('M_Teсh_Burov_DS')

    parser = ParsingData()
    testing_hyp = HypothesisTesting()

    file_path, age, work_days = upload_data_file_and_params()
    
    is_ok, message = parser.parse_file(file_path)
    if not is_ok:
        st.error(f"Загруженный файл не соответсвует требуемому формату. Ошибка: {message}")
        st.stop()
    parser.get_or_update_selections(age, work_days)


    H0_sex, tests_sex = testing_hyp.testing_the_hypothesis_of_avg(parser.data_male, parser.data_female)
    H0_age, tests_age = testing_hyp.testing_the_hypothesis_of_avg(parser.data_more_age, parser.data_less_age)

    testing_hypothesis_and_draw_results(age, work_days, H0_sex, H0_age, tests_sex, tests_age)

    data_plot = [parser.data_male, parser.data_female, parser.data_more_age, parser.data_less_age]
    draw_histograms(data_plot, age)



