from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from ultralytics import YOLO
import shutil
import os
import cv2
import uuid
import base64
import io

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
os.makedirs("results", exist_ok=True)
os.makedirs("uploads", exist_ok=True)

app.mount("/results", StaticFiles(directory="results"), name="results")


model = YOLO("yolov8n.pt")

@app.post("/detect")
async def detect_object(
    image: UploadFile = File(...),
    prompt: str = Form(...)
):
    os.makedirs("uploads", exist_ok=True)
    os.makedirs("results", exist_ok=True)

    file_id = str(uuid.uuid4())
    input_path = f"uploads/{file_id}_{image.filename}"
    output_path = f"results/{file_id}_result.jpg"

    with open(input_path, "wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    img = cv2.imread(input_path)
    results = model(input_path)

    target = prompt.lower().strip()

    found = []

    for r in results:
        print(111111, r.boxes)
        for box in r.boxes:
            class_id = int(box.cls[0])
            name = model.names[class_id]

            print(name, 88888888888)
            confidence = float(box.conf[0])

            if name.lower() == target:
                print (7777)
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

                label = f"{name} {confidence:.2f}"
                cv2.putText(
                    img,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

                found.append({
                    "object": name,
                    "confidence": round(confidence, 3),
                    "box": [x1, y1, x2, y2]
                })

    cv2.imwrite(output_path, img)
    success, buffer = cv2.imencode(".jpg", img)
    if success:

# 2. convert to bytes
        image_bytes = buffer.tobytes()

# 3. base64 encode
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        # print(image_base64)

    return {
        "prompt": prompt,
        "detected": len(found) > 0,
        "results": found,
        "result_img": image_base64

    }