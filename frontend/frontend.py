import streamlit as st 
import requests as re


# -- STREAMLIT INTERFACE --
st.title("⬇Video Downloader")
st.set_page_config(layout= "wide")
st.markdown("---")
st.error("⛔️ There is a possibility that Videos cannot be downloaded such as :\n- Server performance (e.g. large videos)\n- Video hosting platform has strong Security measurements, preventing any downloads.")
url = st.text_input("Enter Video Url here...")
format_choice = st.radio("Choose Type:", ["Video only (Mp4)", "Audio only (Mp3)", "Video and Audio (Mp4)"])

# initializing session states to hold the file data
if "downloaded_file" not in st.session_state:
    st.session_state.downloaded_file = None
if "file_name" not in st.session_state:
    st.session_state.file_name = ""
if "mime_type" not in st.session_state:
    st.session_state.mime_type = ""

try:
    BACKEND_URL = st.secrets.get("BACKEND_URL") # getting the url from Streamlit render
except Exception as e :
    print(f"Error could not secure connection to api: {e}")

# downloading based on format choice of user 
if st.button("Download", icon= "⬇️", width= "stretch"):
    if url :
        if format_choice == "Video only (Mp4)" :
            api_format = "video only"
        elif format_choice == "Audio only (Mp3)":
            api_format = "audio only"
        else:
            api_format = "both"
        
        with st.spinner("Loading..."):
            try:
                api_url = f"{BACKEND_URL}/downloads"
                parameters = {"url": url, "download_type": api_format}
                response = re.get(url= api_url, params= parameters, stream=True) # getting the response from our fastapi 
                
                # creating the output file via the response data and the file extensions 
                if response.ok:
                        # Save to session state
                        ext = "mp3" if api_format == "audio only" else "mp4"
                        st.session_state.mime_type = "audio/mpeg" if api_format == "audio only" else "video/mp4"
                        st.session_state.file_name = f"download.{ext}"
                        st.session_state.downloaded_file = response.content
                        st.success("Video has been downloaded ✅")
                else:
                        st.error(f"Server Error: {response.status_code}")
                        st.error(f"Could not download file: {response.text}")
            except Exception as e:
                    st.error(f"Connection Error: {e}")

# save event outside the scope of the download button
if st.session_state.downloaded_file is not None:
    st.download_button(
        label="Save", 
        icon="💾",
        data=st.session_state.downloaded_file, 
        file_name=st.session_state.file_name,
        mime=st.session_state.mime_type
    )