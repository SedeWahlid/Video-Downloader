import fastapi as fp 
from fastapi.responses import FileResponse
import yt_dlp as yt
import uuid
import os 
import glob

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
    
    # based on users download type we set the options for the download on video only | audio only | video and audio 
    try: 
        if download_type == "both":
            option = {
                'format': 'bestvideo+bestaudio/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'downloads/{file_id}.%(ext)s'}
        elif download_type == "audio only":
            option = {
                'format': 'bestaudio/best',
                'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3','preferredquality': '192',}],
                'outtmpl': f'downloads/{file_id}.%(ext)s'
                }
        elif download_type == "video only":
            option = {
                'format': 'bestvideo/best',
                'merge_output_format': 'mp4',
                'outtmpl': f'downloads/{file_id}.%(ext)s'}
            
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