import io
import os
import uuid
from fastapi import FastAPI, Request, File, UploadFile, Query, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import ffmpeg
import boto3
from botocore.exceptions import BotoCoreError, ClientError
from app.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_S3_BUCKET,
    AWS_REGION,
)

app = FastAPI(title="Woyage AI Audio Extractor")

# mount static files & templates
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

# initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION,
)


@app.get("/")
async def homepage(request: Request):
    """
    Renders the main landing page.
    """
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/video/extract-audio")
async def extract_audio(
    request: Request,
    file: UploadFile = File(...),
    start: float = Query(0.0, ge=0.0, description="Start time in seconds"),
):
    """
    Accepts an MP4 file upload plus a start time,
    extracts audio from start to end as MP3, uploads to S3,
    and returns the S3 key.
    """
    # validate content type
    if file.content_type != "video/mp4":
        raise HTTPException(
            status_code=415, detail="Unsupported file type. Only MP4 allowed."
        )

    # read into memory
    input_bytes = await file.read()
    tmp_in = f"/tmp/{uuid.uuid4()}.mp4"
    tmp_out = f"/tmp/{uuid.uuid4()}.mp3"

    # write temp input
    with open(tmp_in, "wb") as f:
        f.write(input_bytes)

    # run ffmpeg to extract audio
    try:
        (
            ffmpeg.input(tmp_in, ss=start)
            .output(tmp_out, format="mp3", acodec="libmp3lame")
            .overwrite_output()
            .run(quiet=True)
        )
    except ffmpeg.Error as e:
        # clean up and error out
        for p in (tmp_in, tmp_out):
            if os.path.exists(p):
                os.remove(p)
        raise HTTPException(status_code=500, detail="FFmpeg extraction failed.")

    # upload to S3
    base_name = os.path.splitext(file.filename)[0]
    s3_key = f"audio_data/{base_name}.mp3"
    try:
        s3.upload_file(tmp_out, AWS_S3_BUCKET, s3_key)
    except (BotoCoreError, ClientError) as e:
        for p in (tmp_in, tmp_out):
            if os.path.exists(p):
                os.remove(p)
        raise HTTPException(status_code=500, detail="S3 upload failed.")

    # cleanup
    for p in (tmp_in, tmp_out):
        if os.path.exists(p):
            os.remove(p)

    # if JavaScript/XHR form: return JSON; if regular form, re-render with result
    if request.headers.get("accept", "").startswith("application/json"):
        return JSONResponse(
            {
                "result": "success",
                "message": "Audio extracted.",
                "data": {"audio_path": s3_key},
            }
        )
    else:
        # show result on the same landing page
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "result": "Audio extracted successfully!",
                "data": {"audio_path": s3_key},
            },
        )
