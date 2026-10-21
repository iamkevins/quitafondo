from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from rembg import remove
import uuid
import subprocess
import shutil
import os

app = FastAPI()

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.post("/process")
async def process(file: UploadFile = File(...)):

    image_bytes = await file.read()

    uid = str(uuid.uuid4())

    png_file = os.path.join(
        UPLOAD_DIR,
        f"{uid}.png"
    )

    svg_file = os.path.join(
        UPLOAD_DIR,
        f"{uid}.svg"
    )

    no_bg = remove(image_bytes)

    with open(png_file, "wb") as f:
        f.write(no_bg)

    subprocess.run([
        "vtracer",
        "--input",
        png_file,
        "--output",
        svg_file
    ])

    return {
        "png": f"/download/png/{uid}",
        "svg": f"/download/svg/{uid}",
        "preview": f"/files/{uid}.png"
    }


@app.get("/download/png/{uid}")
def download_png(uid: str):

    return FileResponse(
        os.path.join(
            UPLOAD_DIR,
            f"{uid}.png"
        ),
        filename="image.png"
    )


@app.get("/download/svg/{uid}")
def download_svg(uid: str):

    return FileResponse(
        os.path.join(
            UPLOAD_DIR,
            f"{uid}.svg"
        ),
        filename="image.svg"
    )


@app.get("/files/{filename}")
def preview(filename: str):

    return FileResponse(
        os.path.join(
            UPLOAD_DIR,
            filename
        )
    )
