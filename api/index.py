from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import yt_dlp
import assemblyai as aai
from fastapi.middleware.cors import CORSMiddleware
import tempfile

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set AssemblyAI API key from environment variable
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

def get_cookie_path():
    # Look for cookies.txt in the current directory
    cookie_path = os.path.join(os.path.dirname(__file__), "cookies.txt")
    if os.path.exists(cookie_path):
        return cookie_path
    return None

@app.post("/api/transcribe")
async def transcribe(request: Request):
    data = await request.json()
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        return JSONResponse({"error": "youtube_url is required"}, status_code=400)

    # Use system temp directory
    temp_dir = tempfile.gettempdir()
    audio_filename = "downloaded_audio.mp3"
    audio_path = os.path.join(temp_dir, audio_filename)
    audio_base_path = os.path.join(temp_dir, "downloaded_audio")
    
    # Get cookie path
    cookie_path = get_cookie_path()
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'extract_audio': True,
        'audio_format': 'mp3',
        'outtmpl': audio_base_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True,
        # Enhanced options for better reliability
        'nocheckcertificate': True,
        'no_warnings': True,
        'geo_bypass': True,
        'socket_timeout': 30,
        'cookiefile': cookie_path,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        },
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([youtube_url])
    except Exception as e:
        return JSONResponse({"error": f"yt-dlp error: {str(e)}"}, status_code=500)

    if not os.path.exists(audio_path):
        return JSONResponse({"error": "Audio file not found after download"}, status_code=500)

    # Transcribe
    try:
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(audio_path)
        if transcript.status == aai.TranscriptStatus.error:
            return JSONResponse({"error": transcript.error}, status_code=500)
        return JSONResponse({"transcript": transcript.text})
    except Exception as e:
        return JSONResponse({"error": f"Transcription error: {str(e)}"}, status_code=500)

@app.get("/")
async def root():
    return {"message": "YouTube Audio Transcription API"} 