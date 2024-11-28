import streamlit as st
import pandas as pd

# Заголовок страницы
st.title("Сравнение поставщиков")

# Чтение данных
df_providers = pd.read_csv('datasets/providers_quality.csv')

# Уникальные поставщики
unique_providers = ["Все"] + list(df_providers['service_provider'].unique())

# Выбор поставщика
selected_provider = st.selectbox("Выберите поставщика", unique_providers)

# Логика фильтрации
if selected_provider == "Все":
    filtered_providers = df_providers
else:
    filtered_providers = df_providers[df_providers['service_provider'] == selected_provider]

# Вывод результатов
if not filtered_providers.empty:
    if selected_provider == "Все":
        st.write("Информация обо всех поставщиках:")
    else:
        st.write(f"Информация о поставщике: {selected_provider}")

    # Форматированный вывод информации
    for _, row in filtered_providers.iterrows():
        st.markdown(f"### Поставщик: {row['service_provider']}")
        st.write(f"- **Год создания**: {row['year_founded']}")
        st.write(f"- **Количество программ в текущем году**: {row['prog_count_curr_year']}")
        st.write(f"- **Количество слушателей в прошлом году**: {row['number_student_last_year']}")
        st.write(f"- **Количество преподавателей на сайте**: {row['num_teachers_on_website']}")
        st.write("---")
else:
    st.write("Нет поставщиков, соответствующих критериям.")
