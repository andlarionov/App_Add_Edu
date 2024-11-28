import pandas as pd
import streamlit as st

st.title("Поиск образовательной услуги")

# Загружаем данные
df_services = pd.read_csv('datasets/df5.csv')

# Инициализация переменных для фильтров
filtered_data = df_services.copy()

# Первый фильтр: направление деятельности
activity_counts = filtered_data['area_activity'].value_counts()
unique_activity = ["Выбрать"] + [
    f"{activity} ({count})" for activity, count in activity_counts.items()
]
selected_activity = st.selectbox(
    'Вид профессиональной деятельности', 
    unique_activity, 
    index=0
)

if selected_activity != "Выбрать":
    selected_activity = selected_activity.split(" (")[0]  # Убираем часть с количеством
    filtered_data = filtered_data[filtered_data['area_activity'] == selected_activity]

# Второй фильтр: тип образовательной программы
unique_types = ["Выбрать"] + list(filtered_data['type_education'].unique())
selected_type = st.selectbox(
    "Тип образовательной программы", 
    unique_types, 
    index=0
)

if selected_type != "Выбрать":
    filtered_data = filtered_data[filtered_data['type_education'] == selected_type]

# Третий фильтр: форма обучения
unique_forms = ["Выбрать"] + list(filtered_data['service_forms'].unique())
selected_form = st.selectbox(
    "Форма обучения", 
    unique_forms, 
    index=0
)

if selected_form != "Выбрать":
    filtered_data = filtered_data[filtered_data['service_forms'] == selected_form]

# Отображение результатов, если выбраны все фильтры
if (
    selected_activity != "Выбрать" and 
    selected_type != "Выбрать" and 
    selected_form != "Выбрать" and 
    not filtered_data.empty
):
    providers_list = filtered_data['service_provider'].unique()

    for provider in providers_list:
        provider_data = filtered_data[filtered_data['service_provider'] == provider]
        provider_data = provider_data.drop_duplicates(subset=['name_service', 'terms_service', 'classroom_hours', 'service_price'])

        provider_info = provider_data.iloc[0]
        provider_name = provider_info['service_provider']
        phone = provider_info['phone_numbers']
        email = provider_info['e-mail']
        website = provider_info['web_site']

        st.markdown(f"### Поставщик: {provider_name}")
        st.write(f"Телефон: {phone}")
        st.write(f"E-mail: {email}")
        st.write(f"[Сайт]({website})")

        display_data = provider_data[['name_service', 'terms_service', 'classroom_hours', 'service_price']]

        display_data = display_data.rename(columns={
            'name_service': 'Услуга',
            'terms_service': 'Объем услуги',
            'classroom_hours': 'Аудиторные часы',
            'service_price': 'Стоимость'
        })

        st.write("Список услуг:")
        st.write(display_data.to_html(escape=False, index=False), unsafe_allow_html=True)
elif selected_activity == "Выбрать" or selected_type == "Выбрать" or selected_form == "Выбрать":
    st.write("Пожалуйста, выберите значения для всех фильтров.")
else:
    st.write("По вашему запросу ничего не найдено.")

