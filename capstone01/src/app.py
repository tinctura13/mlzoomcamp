import io
import json

from fastapi import FastAPI, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from PIL import Image

from .inpaint import inpaint

app = FastAPI()


@app.get("/")
async def i_am_ok():
    return {"status": "i'm okay, checkout /docs"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/process-image/")
async def process_image(file: bytes = File(...), classes: str = Form(...)):
    try:
        class_thresholds = json.loads(classes)
        
        image = Image.open(io.BytesIO(file))

        if image.mode != 'RGB':
            image = image.convert('RGB')
            
        for class_name, threshold in class_thresholds.items():
            image = inpaint(image, class_name, threshold)

        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        return StreamingResponse(io.BytesIO(img_byte_arr), media_type="image/jpeg")

    except json.JSONDecodeError:
        raise HTTPException(status_code=422, detail="Invalid JSON format in classes")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


origins = [
    "http://localhost:3000",  # Allow your frontend running on localhost:3000
    "http://localhost:8080",  # If you also have frontend components on this port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of origins that are allowed to make requests
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)
