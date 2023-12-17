FROM python:3.10.11-slim-buster

RUN apt-get update && apt-get install -y --no-install-recommends \
    software-properties-common \
    libsm6 libxext6 ffmpeg libfontconfig1 libxrender1 libgl1-mesa-glx \
    curl gcc build-essential

RUN pip install --upgrade pip && \
    pip install torch==1.13.1 torchvision==0.14.1 --extra-index-url https://download.pytorch.org/whl/cpu && \
    pip install --no-cache-dir fastapi uvicorn Pillow python-multipart opencv-python loguru numpy transformers

WORKDIR /

COPY /src /src

EXPOSE 8080

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8080"]
