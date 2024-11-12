import streamlit as st
import pandas as pd
from io import BytesIO

# Заголовок приложения
st.title("Приложение для поиска образовательных услуг")

# Описание приложения
st.write(
    """
    Это приложение помогает пользователю выбрать подходящую программу обучения и образовательную организацию.
    """
)

# Чтение данных из DataFrame df_2 (предполагаем, что он уже загружен)
df = pd.read_csv('datasets/df4.csv')

# Уникальные значения из столбцов
unique_activity = df['area_activity'].unique()
unique_types = df['type_education'].unique()
unique_forms = df['service_forms'].unique()

# Интерактивные элементы управления
area_activity = st.selectbox('Вид профессиональной деятельности', unique_activity)
type_education = st.selectbox("Тип образовательной программы", unique_types)
service_forms = st.selectbox("Форма обучения", unique_forms)

# Фильтрация данных
filtered_data = df[
    (df["area_activity"] == area_activity) &
    (df["type_education"] == type_education) &
    (df["service_forms"] == service_forms)
]

# Если результаты найдены, вывести их
if not filtered_data.empty:
    # Добавление гиперссылок и контактной информации
    filtered_data['Контакты'] = filtered_data.apply(
        lambda row: f'<a href="{row["web_site"]}" target="_blank">{row["service_provider"]}</a><br>'
                    f'Телефон: {row["phone_numbers"]}<br>E-mail: {row["e-mail"]}', axis=1
    )
    
    # Отображение результатов
    st.write("Найденные образовательные услуги:")
    st.write(filtered_data[['Контакты', 'name_service', 'terms_service', 'service_price']].to_html(escape=False), unsafe_allow_html=True)
else:
    st.write("По вашему запросу ничего не найдено.")

# Возможность скачать результаты в формате Excel
if not filtered_data.empty:
    # Создание Excel файла в памяти
    excel_buffer = BytesIO()
    with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
        filtered_data.to_excel(writer, index=False)
    excel_buffer.seek(0)

    # Кнопка для скачивания
    st.download_button(
        label="Скачать результаты в Excel",
        data=excel_buffer,
        file_name='results.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
