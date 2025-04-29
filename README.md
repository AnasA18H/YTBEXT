# YouTube Transcription API

A FastAPI-based API for YouTube video transcription using AssemblyAI.

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables:
   - `ASSEMBLYAI_API_KEY` - Your AssemblyAI API key

3. (Optional) Add cookies.txt:
   - Place a `cookies.txt` file in the `api` directory
   - This file should contain your YouTube cookies in Netscape format
   - This helps bypass YouTube's bot detection

## Local Development

Run the local test server:
```
python local_test.py
```

## API Endpoints

### POST /api/transcribe
Transcribes audio from a YouTube video.

**Request Body:**
```json
{
  "youtube_url": "https://www.youtube.com/watch?v=YOUTUBE_VIDEO_ID"
}
```

**Response:**
```json
{
  "transcript": "The transcribed text will appear here."
}
```

## Testing with Postman

1. Create a POST request to `http://localhost:8000/api/transcribe`
2. Set the request body to JSON with a `youtube_url` property
3. Send the request and receive the transcription

## Deployment to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure the service:
   - Name: youtube-transcription-api
   - Environment: Python
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn api.index:app --host 0.0.0.0 --port $PORT`
   - Add Environment Variable:
     - Key: `ASSEMBLYAI_API_KEY`
     - Value: Your AssemblyAI API key

4. Deploy the service

The API will be available at your Render URL (e.g., `https://youtube-transcription-api.onrender.com`)

## Alternative Deployment Options

This API can also be deployed to other platforms that support Python applications, such as:
- Heroku
- DigitalOcean
- AWS
- Google Cloud Platform
- Any VPS or dedicated server

Make sure to:
1. Set the `ASSEMBLYAI_API_KEY` environment variable
2. Configure your platform's proxy settings if needed
3. Set up proper CORS settings for your domain
4. Consider using a process manager like PM2 or Supervisor 