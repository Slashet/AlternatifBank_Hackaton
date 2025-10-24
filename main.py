import re
import asyncio
from fastapi import FastAPI
from fastapi.responses import HTMLResponse, FileResponse
from concurrent.futures import ThreadPoolExecutor
from backend.speech_worker import speech
from backend.Text.text_analyse import *
from backend.server_service import *
from backend.talk_worker import *
from backend.request import *
from backend.camera_capture import *
import cv2
import threading
import time

app = FastAPI()
executor = ThreadPoolExecutor(max_workers=4)
current_action = ""  # Yeni global değişken

class ContinuousCamera:
    def __init__(self, device=0):
        self.device = device
        self.cap = None
        self._stop_event = threading.Event()
        
    def start(self):
        self.cap = cv2.VideoCapture(self.device, cv2.CAP_DSHOW)
        if not self.cap.isOpened():
            raise RuntimeError("Kamera açılamadı")
            
    def stop(self):
        self._stop_event.set()
        if self.cap:
            self.cap.release()
            
    def read_frame(self):
        if not self.cap or not self.cap.isOpened():
            return None
        ret, frame = self.cap.read()
        if not ret:
            return None
        ok, buf = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
        if not ok:
            return None
        return buf.tobytes()

# Global kamera nesnesi
camera = None

async def camera_background_task():
    global camera, current_action
    loop = asyncio.get_event_loop()
    
    try:
        camera = ContinuousCamera(device=0)
        await loop.run_in_executor(executor, camera.start)
        
        while True:
            frame_bytes = await loop.run_in_executor(executor, camera.read_frame)
            if frame_bytes:
                try:
                    result = await loop.run_in_executor(executor, upload_image_bytes, frame_bytes)
                    predictions = result.get("predictions", [])
                    filtered_preds = [p for p in predictions if p.get("probability", 0) > 0.6]
                    if filtered_preds:
                        if filtered_preds[0]['tagName'] == "para gönder":
                            current_action = "transfer"
                            print("Para gönderme işlemi tespit edildi")
                        elif filtered_preds[0]['tagName'] == "kredi":
                            current_action = "credit"
                            print("Kredi işlemi tespit edildi")
                except Exception as e:
                    print(f"Upload hatası: {e}")
            await asyncio.sleep(0.2)  # Saniyede 5 request
            
    except Exception as e:
        print(f"Kamera hatası: {e}")
    finally:
        if camera:
            await loop.run_in_executor(executor, camera.stop)

async def background_task():
    global current_message, status_message
    loop = asyncio.get_event_loop()

    try:
        while True:
            status_message = "Dinleniyor..."
            text = await loop.run_in_executor(executor, speech)
            if text:
                processed_text = process_text(text)
                match = re.search(r"\{(.*?)\}", processed_text)
                text_1 = match.group(0) if match else ""
                text_2 = re.sub(r"\{.*?\}", "", processed_text).strip()
                current_message = text_2
                await loop.run_in_executor(executor, talk, text_2)
                print("Parantez içi:", text_1)
            await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        return

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(background_task())
    asyncio.create_task(camera_background_task())

@app.on_event("shutdown")
async def shutdown_event():
    global camera
    if camera:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(executor, camera.stop)

@app.get("/", response_class=HTMLResponse)
async def home():
    return FileResponse("index.html")

@app.get("/current_action")
async def get_current_action():
    global current_action
    action = current_action
    current_action = ""  # Sıfırla
    return {"action": action}