import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from pathlib import Path

sns.set(style='dark')

st.subheader("Data")
def by_workingday_df(df):
    byworkingday_bike = df.groupby(by="workingday").instant.nunique().reset_index()
    byworkingday_bike.rename(columns={"instant": "sum"}, inplace=True)
    byworkingday_bike

    return byworkingday_bike


def by_weather_df(df):
    byseason_bike = df.groupby(by="weathersit").instant.nunique().reset_index()
    byseason_bike.rename(columns={"instant": "sum"}, inplace=True)
    byseason_bike

    return byseason_bike


def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()
    with st.sidebar:
        # Menambahkan logo perusahaan
        st.image("https://www.brandcrowd.com/blog/wp-content/uploads/2019/06/bike-share.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )

    return date

# load dataset
day_bike = pd.read_csv("dashboard.csv")

date = sidebar(day_bike)
if len(date) == 2:
    main_df = day_bike[(day_bike["dteday"] >= str(date[0])) & (day_bike["dteday"] <= str(date[1]))]
else:
    main_df = day_bike[
        (day_bike["dteday"] >= str(st.session_state.date[0])) & (day_bike["dteday"] <= str(st.session_state.date[1]))]

byworkingday_bike = by_workingday_df(main_df)
byseason_bike = by_weather_df(main_df)


# pengaruh hari kerja mempengeruhi pengunaan bike sharing
st.header("Bike Sharing Dashboard :bike:")
st.subheader("Working Day")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="workingday",
    data=byworkingday_bike.sort_values(by="workingday", ascending=False),
    ax=ax
)
ax.set_title("Bagaimana pengaruh hari kerja mempengeruhi pengunaan bike sharing?", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel(None)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

# kondisi musim terhadap banyaknya pengguna bike sharing
st.subheader("Weather")
fig, ax = plt.subplots(figsize=(20, 10))
sns.barplot(
    y="sum",
    x="weathersit",
    data=byseason_bike.sort_values(by="weathersit", ascending=False),
)
ax.set_title("Bagaimana kondisi cuaca terhadap banyaknya pengguna bike sharing?", loc="center", fontsize=15)
ax.set_ylabel("Jumlah Pengguna")
ax.set_xlabel(None)
ax.tick_params(axis="x", labelsize=20)
ax.tick_params(axis="y", labelsize=15)
st.pyplot(fig)

if __name__ == "__main__":
    copyright = "Copyright © " + "2023 | Bike Sharing Dashboard | All Rights Reserved | " + "Made by: [@dinar_wahyu](https://https://www.linkedin.com/in/dinar-wahyu-rahman-00a405162/)"
    st.caption(copyright)
