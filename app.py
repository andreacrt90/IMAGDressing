from fastapi import FastAPI, UploadFile, File, HTTPException
import uuid, shutil, os, subprocess, sys

app = FastAPI()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.post("/tryon")
async def tryon(person: UploadFile = File(...), dress: UploadFile = File(...)):
    try:
        # --- Salvataggio file ---
        person_path = os.path.join(UPLOAD_DIR, f"person_{uuid.uuid4()}.png")
        dress_path = os.path.join(UPLOAD_DIR, f"dress_{uuid.uuid4()}.png")
        output_path = os.path.join(OUTPUT_DIR, f"result_{uuid.uuid4()}.png")

        with open(person_path, "wb") as f:
            shutil.copyfileobj(person.file, f)
        with open(dress_path, "wb") as f:
            shutil.copyfileobj(dress.file, f)

        # --- Esecuzione script ---
        cmd = [
            sys.executable, 
            "inference_IMAGdressing_ipa_controlnetpose.py",
            "--cloth_path", dress_path,
            "--face_path", person_path
        ]

        process = subprocess.run(cmd, capture_output=True, text=True)

        if process.returncode != 0:
            # Se lo script fallisce, alza errore HTTP
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Script execution failed",
                    "command": " ".join(cmd),
                    "stderr": process.stderr
                }
            )

        # --- Verifica esistenza output ---
        if not os.path.exists(output_path):
            raise HTTPException(
                status_code=500,
                detail={
                    "error": "Output file not generated",
                    "expected_path": output_path
                }
            )

        return {"status": "ok", "result": output_path}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
