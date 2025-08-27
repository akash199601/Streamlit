import requests
import streamlit as st

st.title("Bulk MP3 Downloader")

uploaded_file = st.file_uploader("Upload URLs TXT file", type="txt")

if uploaded_file is not None:
    urls = uploaded_file.read().decode("utf-8").splitlines()
    
    if st.button("Start Download"):
        for i, url in enumerate(urls, start=1):
            try:
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    filename = f"recording_{i}.mp3"
                    with open(filename, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)
                    st.write(f"✅ Downloaded: {filename}")
                else:
                    st.write(f"❌ Failed: {url}")
            except Exception as e:
                st.write(f"⚠️ Error: {e}")
        st.success("All recordings downloaded!")
