import fastapi as fp 
from fastapi.responses import FileResponse
from fastapi import HTTPException
import yt_dlp as yt
import uuid
import os 
import glob
import tempfile

# -- VIDEO/AUDIO DOWNLOADER -- 

app = fp.FastAPI()

# deleting/removing the file from the server 
def cleanup(path: str):
    if os.path.exists(path):
        os.remove(path)
        print(f"Deleted temp file: {path}")

@app.get("/downloads")
def download_video(url:str,download_type:str, background_tasks : fp.BackgroundTasks):
    file_id = str(uuid.uuid4()) # creating a unique ID for the file 
    
    cookie_temp_file = None
    cookies_content = os.environ.get("YOUTUBE_COOKIES")
    if cookies_content:
        # creating a temporary file to hold the cookies
        # delete=False is needed so we can close the file and let yt-dlp open it again
        cookie_temp_file = tempfile.NamedTemporaryFile(mode='w+', delete=False, suffix='.txt')
        cookie_temp_file.write(cookies_content)
        cookie_temp_file.close() 
        print(f"Cookies loaded to temp file:{cookie_temp_file.name}")

    # definiton of user agents 
    my_user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    
    # based on users download type we set the options for the download on video only | audio only | video and audio 
    try: 
        base_opts = {
            'outtmpl': f'downloads/{file_id}.%(ext)s',
            'user_agent': my_user_agent,
            # If cookie file exists we use it if not we wont.
            'cookiefile': cookie_temp_file.name if cookie_temp_file else None}
        if download_type == "both":
            option = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'downloads/{file_id}.%(ext)s',**base_opts}
        elif download_type == "audio only":
            option = {
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],
                'outtmpl': f'downloads/{file_id}.%(ext)s',**base_opts}
        elif download_type == "video only":
            option = {
                'format': 'bestvideo/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'downloads/{file_id}.%(ext)s',**base_opts}
            
        os.makedirs("downloads", exist_ok=True) # making sure that directory exists for the output files 
        
        with yt.YoutubeDL(option) as ytdl:
            ytdl.download([url]) 
            
            files = glob.glob(f"downloads/{file_id}*")
            filename_path = files[0]
            
            # get the actual extension found 
            target_ext = filename_path.split('.')[-1]
            infos = ytdl.extract_info(url, download=False)
            
            # cleaning filename for user
            title = infos.get('title', 'download')
            safe_filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
            user_filename = f"{safe_filename}.{target_ext}"
            
            # checking if file is within the server
            if not user_filename:
                raise(Exception("Download successful but file not found within server."))
            
            if target_ext == "mp3":
                mime_type = "audio/mpeg"
            else:
                mime_type = "video/mp4"
            
            background_tasks.add_task(cleanup, filename_path) # deleting file after response to not cause server memory overload
            
            return FileResponse(path=filename_path,filename= user_filename, media_type = mime_type)
    except Exception as e :
        print(f"ERROR could not download video: {e}")
        raise HTTPException(status_code=500, detail=f"Server Error: {str(e)}")
    finally:
        # deleting the temp cookie file so it does not fill up the server
        if cookie_temp_file and os.path.exists(cookie_temp_file.name):
            os.remove(cookie_temp_file.name)
            print("cleaned...")