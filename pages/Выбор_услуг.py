import pandas as pd
import streamlit as st


st.title("Поиск образовательной услуги")


df_services = pd.read_csv('datasets/df5.csv')
df_providers = pd.read_csv('datasets/providers_quality.csv')


# Подсчёт количества программ для каждого направления
activity_counts = df_services['area_activity'].value_counts()

# Список направлений с количеством программ
unique_activity = ["Выбрать"] + [
    f"{activity} ({count})" for activity, count in activity_counts.items()
]
unique_types = ["Выбрать"] + list(df_services['type_education'].unique())
unique_forms = ["Выбрать"] + list(df_services['service_forms'].unique())

# Интерактивные элементы управления
area_activity = st.selectbox('Вид профессиональной деятельности', unique_activity)
type_education = st.selectbox("Тип образовательной программы", unique_types)
service_forms = st.selectbox("Форма обучения", unique_forms)

# Извлечение направлений без цифры в скобках
if area_activity != "Выбрать":
    area_activity = area_activity.split(" (")[0]  # Убираем часть после названия
else:
    area_activity = None

# Инициализация пустого DataFrame для случая, если фильтрация не производится
filtered_data = pd.DataFrame()

# Проверяем, чтобы пользователь сделал выбор
if area_activity and type_education != "Выбрать" and service_forms != "Выбрать":
    # Фильтрация данных
    filtered_data = df_services[
        (df_services["area_activity"] == area_activity) & 
        (df_services["type_education"] == type_education) & 
        (df_services["service_forms"] == service_forms)
    ]

# Отображаем результаты только если фильтрация вернула данные
if not filtered_data.empty:
    # Уникальные поставщики из отфильтрованных данных
    providers_list = filtered_data['service_provider'].unique()

    # Для каждого поставщика выводим данные
    for provider in providers_list:
        # Получаем все услуги для данного поставщика
        provider_data = filtered_data[filtered_data['service_provider'] == provider]
        
        # Убираем дубликаты по всем столбцам
        provider_data = provider_data.drop_duplicates(subset=['name_service', 'terms_service', 'classroom_hours', 'service_price'])
        
        # Разделяем контактные данные
        provider_info = provider_data.iloc[0]
        
        # Название поставщика и контактная информация
        provider_name = provider_info['service_provider']
        phone = provider_info['phone_numbers']
        email = provider_info['e-mail']
        website = provider_info['web_site']
        
        # Отображаем имя поставщика и контакты
        st.markdown(f"### Поставщик: {provider_name}")
        st.write(f"Телефон: {phone}")
        st.write(f"E-mail: {email}")
        st.write(f"[Сайт]({website})")
        
        # Подготовка данных для отображения
        display_data = provider_data[['name_service', 'terms_service', 'classroom_hours', 'service_price']]

        # Переименовываем колонки на русский язык
        display_data = display_data.rename(columns={
            'name_service': 'Услуга',
            'terms_service': 'Объем услуги',
            'classroom_hours': 'Аудиторные часы',
            'service_price': 'Стоимость'
        })

        # Выводим таблицу
        st.write("Список услуг:")
        st.write(display_data.to_html(escape=False, index=False), unsafe_allow_html=True)
elif area_activity is None or type_education == "Выбрать" or service_forms == "Выбрать":
    st.write("Пожалуйста, выберите значения для всех фильтров.")
else:
    st.write("По вашему запросу ничего не найдено.")