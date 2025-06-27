# Woyage AI Audio Extractor (Web)

A responsive FastAPI + Jinja2 web application that lets you upload an MP4 video, specify a start time, extract the audio as an MP3, and securely store it in your AWS S3 bucket.

## 🎥 Demo

Watch a quick walkthrough of this project on Loom:  
👉 [Demo Video](https://www.loom.com/share/7501683938994f5c81585a28aef1c0ee?sid=a2bd5373-34c4-49cd-a0f2-4206b6f06a3c)

---

## Prerequisites

- **Python 3.8+**  
- **FFmpeg** installed and on your PATH  
- **AWS** account with:  
  - An S3 bucket (e.g. `woyage-audio-bucket`) in your chosen region (e.g. `us-east-2`)  
  - An IAM user with **Programmatic access** and S3 PUT permissions  

## Setup & Installation

1. **Clone the repository**  
   ```bash
   git clone https://github.com/your-org/woyage-ai-audio-extractor.git
   cd woyage-ai-audio-extractor

2. **Create and activate a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate        # macOS/Linux
   .\venv\Scripts\Activate.ps1     # Windows PowerShell

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt

4. **Create and populate .env**

   In the project root, create a file named `.env` with:
   ```dotenv
   AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY_ID
   AWS_SECRET_ACCESS_KEY=YOUR_SECRET_ACCESS_KEY
   AWS_S3_BUCKET=your-s3-bucket-name
   AWS_REGION=us-east-2
   ```
5. **Verify FFmpeg installation**
   ```bash
   ffmpeg -version

6. **Run the application**
   ```bash
   uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

7. **Open in your browser**

   Navigate to http://127.0.0.1:8000 and upload an MP4 to test!

## Project Structure
   ```bash
   woyage-ai-audio-extractor/
├── app/
│   ├── main.py          # FastAPI endpoints & FFmpeg/S3 logic
│   ├── config.py        # dotenv loader & AWS settings
│   ├── static/          # CSS & assets
│   │   └── style.css
│   └── templates/       # Jinja2 HTML templates
│       └── index.html
├── .env                 # AWS credentials & bucket info (ignored by Git)
├── .gitignore
├── README.md
└── requirements.txt
   ```
## How It Works

- **Frontend**  
  Serves a single‐page form (Jinja2) allowing drag-and-drop or file browse for MP4 plus a start-time input.

- **Upload**  
  User submits video and start time to the `/video/extract-audio` endpoint.

- **Extraction**  
  FastAPI reads the MP4 into a temp file and invokes FFmpeg to extract audio from the specified timestamp to the end, saving an MP3.

- **Upload to S3**  
  The MP3 is uploaded to your S3 bucket under the key `audio_data/<video-name>.mp3`, using boto3 with your `.env` credentials.

- **Response**  
  Returns JSON to API clients:
  ```json
  {
    "result": "success",
    "message": "Audio extracted.",
    "data": {
      "audio_path": "audio_data/…"
    }
  }
  ```
  or re-renders the page with a success banner and the S3 key.

## Next Steps

- 🔒 **Tighten IAM permissions**  
  Replace `AmazonS3FullAccess` with a scoped policy limited to your bucket.

- 🚀 **Production deploy**  
  Containerize with Docker and deploy behind an HTTPS-enabled load balancer.

- 📊 **Monitoring**  
  Configure AWS CloudWatch alarms for failed extractions or S3 upload errors.

- 🧹 **Cleanup**  
  Implement S3 lifecycle rules to auto-expire or archive old MP3s automatically.

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).  
See the full terms on the [Open Source Initiative website](https://opensource.org/licenses/MIT).  

© 2025 Raymond Li
