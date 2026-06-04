import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import yt_dlp

app = FastAPI(title="SK-Downloader Cloud Engine")

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
    return {"status": "SK-Engine Cloud is Live and Free, Sher Khan!"}

@app.post("/extract")
def extract_video_url(request: VideoRequest):
    video_url = request.url.strip()
    pref = request.format_preference
    platform = request.platform
    
    if not video_url:
        raise HTTPException(status_code=400, detail="URL cannot be empty")
        
    # Advanced extraction rules based on user choice
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }

    if pref == "Audio_MP3":
        ydl_opts['format'] = 'bestaudio/best'
    elif pref == "No_Watermark" and platform == "TikTok":
        # TikTok no watermark dynamic fetch
        ydl_opts['format'] = 'bestvideo'
    else:
        ydl_opts['format'] = 'best' # Standard HD Video combine
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Streaming link generation
            direct_url = info.get('url')
            title = info.get('title', f"SK_{platform}_File")
            
            if not direct_url:
                # Fallback check if links are nested in formats array
                formats = info.get('formats', [])
                if formats:
                    direct_url = formats[-1].get('url')
            
            if not direct_url:
                raise HTTPException(status_code=404, detail="Could not extract direct media link")
                
            return {
                "success": True,
                "title": title,
                "download_url": direct_url
            }
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SK-Engine extraction failed: {str(e)}")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)