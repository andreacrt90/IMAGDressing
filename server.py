from fastapi import FastAPI, UploadFile, File
import shutil
import os
from inference import process_image  # Funzione che esegue il try-on con IMAGDressing

app = FastAPI()

@app.post("/upload/")
async def upload_image(user: UploadFile = File(...), cloth: UploadFile = File(...)):
    user_path = f"temp/{user.filename}"
    cloth_path = f"temp/{cloth.filename}"
    
    with open(user_path, "wb") as buffer:
        shutil.copyfileobj(user.file, buffer)
    with open(cloth_path, "wb") as buffer:
        shutil.copyfileobj(cloth.file, buffer)
    
    result_path = process_image(user_path, cloth_path)  # Genera l'immagine con vestito applicato
    return {"image_url": f"/static/{result_path}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
