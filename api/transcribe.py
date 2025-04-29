import os
import yt_dlp
import assemblyai as aai
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

# Set AssemblyAI API key from environment variable
aai.settings.api_key = os.environ.get("ASSEMBLYAI_API_KEY")

@app.post("/api/transcribe")
async def transcribe(request: Request):
    data = await request.json()
    youtube_url = data.get("youtube_url")
    if not youtube_url:
        return JSONResponse({"error": "youtube_url is required"}, status_code=400)

    # Download audio to /tmp (Vercel writable dir)
    audio_path = "/tmp/downloaded_audio.mp3"
    ydl_opts = {
        'format': 'bestaudio/best',
        'extract_audio': True,
        'audio_format': 'mp3',
        'outtmpl': '/tmp/downloaded_audio',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
        'quiet': True,
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