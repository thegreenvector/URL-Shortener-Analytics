import streamlit as st
import requests
import pandas as pd
import plotly.express as px

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="URL Shortener", page_icon="🔗", layout="wide")

st.title("🔗 URL Shortener & Analytics")
st.write("Create shortened URLs and track their performance.")

st.subheader("Create a Short URL")

url = st.text_input("Enter a long URL", placeholder="https://www.wikipedia.org")

if st.button("Shorten URL", type="primary"):
    if url:
        try:
            response = requests.post(f"{API_URL}/shorten", json={"url": url}, timeout=10)
            response.raise_for_status()
            data = response.json()
            st.success("Short URL created successfully!")
            st.code(data["short_url"])
        except requests.exceptions.RequestException as e:
            st.error(f"Unable to shorten URL: {e}")
    else:
        st.warning("Please enter a URL.")

st.divider()
st.subheader("📊 Analytics Dashboard")

if st.button("Refresh Analytics"):
    st.rerun()

try:
    response = requests.get(f"{API_URL}/analytics", timeout=10)
    response.raise_for_status()
    records = response.json()

    if records:
        df = pd.DataFrame(records)
        df["created_at"] = pd.to_datetime(df["created_at"])

        total_urls = len(df)
        total_clicks = int(df["clicks"].sum())
        average_clicks = round(total_clicks / total_urls, 2)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total URLs", total_urls)
        col2.metric("Total Clicks", total_clicks)
        col3.metric("Average Clicks", average_clicks)

        st.subheader("Click Performance")

        fig = px.bar(
            df,
            x="short_code",
            y="clicks",
            color="clicks",
            title="Clicks per Shortened URL",
            labels={"short_code": "Short Code", "clicks": "Clicks"}
        )
        st.plotly_chart(fig, use_container_width=True)

        st.subheader("URL Records")
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False)
        st.download_button(
            "Download Analytics CSV",
            csv,
            "url_analytics.csv",
            "text/csv"
        )
    else:
        st.info("No shortened URLs yet. Create your first one!")

except requests.exceptions.RequestException:
    st.error("Cannot connect to FastAPI. Make sure the backend is running.")