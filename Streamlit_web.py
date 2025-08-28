# import requests
# import streamlit as st

# st.title("Bulk MP3 Downloader")

# uploaded_file = st.file_uploader("Upload URLs TXT file", type="txt")

# if uploaded_file is not None:
#     urls = uploaded_file.read().decode("utf-8").splitlines()
    
#     if st.button("Start Download"):
#         for i, url in enumerate(urls, start=1):
#             try:
#                 response = requests.get(url, stream=True)
#                 if response.status_code == 200:
#                     filename = f"recording_{i}.mp3"
#                     with open(filename, "wb") as file:
#                         for chunk in response.iter_content(1024):
#                             file.write(chunk)
#                     st.write(f"✅ Downloaded: {filename}")
#                 else:
#                     st.write(f"❌ Failed: {url}")
#             except Exception as e:
#                 st.write(f"⚠️ Error: {e}")
#         st.success("All recordings downloaded!")
import requests
import streamlit as st
import io
import zipfile
import time

st.title("Bulk MP3 Downloader (ZIP)")

uploaded_file = st.file_uploader("Upload URLs TXT file", type="txt")

if uploaded_file is not None:
    urls = uploaded_file.read().decode("utf-8").splitlines()
    
    if st.button("Start Download"):
        zip_buffer = io.BytesIO()            # In-memory ZIP
        total_files = len(urls)
        progress_bar = st.progress(0)        # Progress bar
        status_text = st.empty()             # Status message
        
        with st.spinner("Downloading MP3s and creating ZIP..."):
            with zipfile.ZipFile(zip_buffer, "w") as zip_file:
                for i, url in enumerate(urls, start=1):
                    try:
                        response = requests.get(url, stream=True)
                        if response.status_code == 200:
                            filename = f"recording_{i}.mp3"
                            zip_file.writestr(filename, response.content)  # Add to ZIP in memory
                            status_text.text(f"✅ Added {filename} to ZIP ({i}/{total_files})")
                        else:
                            status_text.text(f"❌ Failed to download: {url}")
                    except Exception as e:
                        status_text.text(f"⚠️ Error: {e}")
                    
                    progress_bar.progress(i / total_files)
                    time.sleep(0.05)  # Optional: visual feedback

            zip_buffer.seek(0)  # Reset buffer pointer

        st.success("All recordings are ready!")
        st.download_button(
            label="Download All MP3s as ZIP",
            data=zip_buffer,
            file_name="all_recordings.zip",
            mime="application/zip"
        )
        