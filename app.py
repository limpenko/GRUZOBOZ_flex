import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Автопарк Грузовоз | Мониторинг",
    page_icon="🚛",
    layout="wide",
)

st.title("🚛 АВТОПАРК ГРУЗОВОЗ — Мониторинг рейсов и статусов")
st.markdown("Оперативная сводка по транспорту, водителям и направлениям.")


@st.cache_data
def load_data():
  if not os.path.exists("data.xlsx"):
    with pd.ExcelWriter("data.xlsx", engine="openpyxl") as writer:
      df_t = pd.DataFrame(columns=[
          "Г/Н",
          "МОДЕЛЬ",
          "ПРИЦЕП",
          "СТАТУС АВТОМОБИЛЯ",
          "ВОДИТЕЛЬ",
          "НОМЕР",
          "ПОГРУЗКА",
          "ДАТА",
          "ВЫГРУЗКА",
          "ДАТА.",
          "СЛЕД.ПОГРУЗКА",
      ])
      df_t.to_excel(writer, sheet_name="Sheet1", index=False)

  # Читаем самый первый лист из вашего Excel-файла (без привязки к имени листа)
  try:
    trucks_df = pd.read_excel("data.xlsx", sheet_name=0)
  except Exception as e:
    trucks_df = pd.DataFrame()

  return trucks_df


df_trucks = load_data()

st.subheader("Текущее состояние и статусы транспорта")
if df_trucks.empty:
  st.warning(
      "Таблица пуста или файл не прочитан. Проверьте заполнена ли таблица"
      " data.xlsx."
  )
else:
  # Выводим таблицу целиком
  st.dataframe(df_trucks, use_container_width=True)

  st.divider()
  st.subheader("🔍 Быстрый поиск по транспорту")
  if "Г/Н" in df_trucks.columns:
    # Убираем возможные пустые строчки
    valid_gns = df_trucks["Г/Н"].dropna().unique()
    chosen_truck = st.selectbox("Выберите госномер ТС:", valid_gns)

    car_row = df_trucks[df_trucks["Г/Н"] == chosen_truck].iloc[0]

    col1, col2, col3 = st.columns(3)
    with col1:
      st.info(
          f"**Модель:** {car_row.get('МОДЕЛЬ', '-')}\n\n**Прицеп:**"
          f" {car_row.get('ПРИЦЕП', '-')}"
      )
    with col2:
      st.success(
          f"**Статус:** {car_row.get('СТАТУС АВТОМОБИЛЯ', '-')}\n\n**Водитель:**"
          f" {car_row.get('ВОДИТЕЛЬ', '-')}"
      )
    with col3:
      st.warning(
          f"**Телефон:** `{car_row.get('НОМЕР', '-')}`\n\n**Маршрут:**"
          f" {car_row.get('ПОГРУЗКА', '-')} ➔ {car_row.get('ВЫГРУЗКА', '-')}"
      )