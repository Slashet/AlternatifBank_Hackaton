# ...existing code...
import time
import cv2

def capture_one_second(device=0, duration=1.0, max_fps=30, return_jpeg=True):
    """
    Kamerayı açar ve verilen süre (varsayılan 1.0 saniye) boyunca kareleri yakalar.
    Parametreler:
      - device: kamera cihaz numarası (varsayılan 0)
      - duration: yakalama süresi (saniye)
      - max_fps: yakalama hızını sınırlamak için maksimum FPS (None veya 0 => sınırlama yok)
      - return_jpeg: True ise JPEG byte'ları listesi döner, False ise BGR numpy array listesi döner

    Dönen değer: yakalanan karelerin listesi
    """
    cap = cv2.VideoCapture(device, cv2.CAP_DSHOW)  # Windows'ta daha az gecikme için DS_SHOW kullanalım
    if not cap.isOpened():
        raise RuntimeError("Kamera açılamadı. Cihaz numarasını kontrol edin veya başka bir uygulama kullanmıyor mu bakın.")

    frames = []
    start = time.time()
    try:
        while time.time() - start < duration:
            ret, frame = cap.read()
            if not ret:
                break
            # kopyasını alıyoruz, böylece OpenCV'nin iç buffer'ı değişse bile elimizde sabit veri olur
            if return_jpeg:
                ok, buf = cv2.imencode('.jpg', frame, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
                if not ok:
                    continue
                frames.append(buf.tobytes())
            else:
                frames.append(frame.copy())

            if max_fps and max_fps > 0:
                time.sleep(1.0 / max_fps)
    finally:
        cap.release()

    return frames
