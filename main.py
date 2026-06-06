import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import yt_dlp

app = FastAPI(title="SK-Downloader Cloud Engine")

# CORS setup critical for mobile apps connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoRequest(BaseModel):
    url: str
    format_preference: Optional[str] = "HD_Video"
    platform: Optional[str] = "YouTube"

@app.get("/")
def home():
    return {"status": "SK-Engine Cloud is Live with Cookies Session, Sher Khan!"}

@app.post("/extract")
def extract_video_url(request: VideoRequest):
    video_url = request.url.strip()
    pref = request.format_preference
    platform = request.platform
    
    if not video_url:
        raise HTTPException(status_code=400, detail="URL khali hai, please link dalein")
        
    # ANTI-BOT BYPASS: Safe Headers setup
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
        'extract_flat': False,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    # CRITICAL INJECTION: Checking for cookies.txt file
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = 'cookies.txt'

    # Format handling overrides based on user choice
    if pref == "Audio_MP3":
        ydl_opts['format'] = 'bestaudio/best'
    elif pref == "No_Watermark" and platform == "TikTok":
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
    else:
        ydl_opts['format'] = 'best/bestvideo+bestaudio'
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Dynamic URL extraction logic
            direct_url = info.get('url')
            title = info.get('title', f"SK_{platform}_File")
            
            if not direct_url and 'formats' in info:
                valid_formats = [f for f in info['formats'] if f.get('url')]
                if valid_formats:
                    direct_url = valid_formats[-1]['url']
            
            if not direct_url:
                raise HTTPException(status_code=404, detail="Direct streaming link nahi mil saka")
                
            return {
                "success": True,
                "title": title,
                "download_url": direct_url
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"yt-dlp Engine Alert: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
