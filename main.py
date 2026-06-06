import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import os
import yt_dlp

app = FastAPI(title="SK-Downloader Cloud Engine")

# CORS setup critical for mobile apps connection[cite: 2]
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
    video_url = request.url.strip()[cite: 2]
    pref = request.format_preference[cite: 2]
    platform = request.platform[cite: 2]
    
    if not video_url:[cite: 2]
        raise HTTPException(status_code=400, detail="URL khali hai, please link dalein")[cite: 2]
        
    # ANTI-BOT BYPASS: Safe Headers setup[cite: 2]
    ydl_opts = {
        'quiet': True,[cite: 2]
        'no_warnings': True,[cite: 2]
        'extract_flat': False,[cite: 2]
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Sec-Fetch-Mode': 'navigate',
        }
    }

    # CRITICAL INJECTION: Agar repo mein cookies.txt hai toh usey yt-dlp ke opts mein inject karo
    if os.path.exists("cookies.txt"):
        ydl_opts['cookiefile'] = 'cookies.txt'

    # Format handling overrides based on user choice[cite: 2]
    if pref == "Audio_MP3":[cite: 2]
        ydl_opts['format'] = 'bestaudio/best'[cite: 2]
    elif pref == "No_Watermark" and platform == "TikTok":[cite: 2]
        ydl_opts['format'] = 'bestvideo+bestaudio/best'[cite: 2]
    else:[cite: 2]
        ydl_opts['format'] = 'best/bestvideo+bestaudio'[cite: 2]
    
    try:[cite: 2]
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:[cite: 2]
            info = ydl.extract_info(video_url, download=False)[cite: 2]
            
            # Dynamic URL extraction logic[cite: 2]
            direct_url = info.get('url')[cite: 2]
            title = info.get('title', f"SK_{platform}_File")[cite: 2]
            
            if not direct_url and 'formats' in info:[cite: 2]
                # Fallback filter if urls are nested deep inside formats array[cite: 2]
                valid_formats = [f for f in info['formats'] if f.get('url')][cite: 2]
                if valid_formats:[cite: 2]
                    direct_url = valid_formats[-1]['url'][cite: 2]
            
            if not direct_url:[cite: 2]
                raise HTTPException(status_code=404, detail="Direct streaming link nahi mil saka")[cite: 2]
                
            return {[cite: 2]
                "success": True,[cite: 2]
                "title": title,[cite: 2]
                "download_url": direct_url[cite: 2]
            }[cite: 2]
            
    except Exception as e:[cite: 2]
        # Detailed error forward to Flutter UI for easy debugging[cite: 2]
        raise HTTPException(status_code=500, detail=f"yt-dlp Engine Alert: {str(e)}")[cite: 2]

if __name__ == "__main__":[cite: 2]
    uvicorn.run("main:app", host="0.0.0.0", port=8000)[cite: 2]
